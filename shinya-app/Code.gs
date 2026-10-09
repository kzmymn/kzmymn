/**
 * 深夜・休日出勤カレンダー（Google Apps Script）
 *
 * 使い方：記録用のGoogleスプレッドシートを開き「拡張機能 > Apps Script」にこのファイルと Index.html を貼り付けます。
 * 手順は README.md を参照してください。
 *
 * ・Webアプリは「自分（デプロイした人）として実行」します。メンバーにスプレッドシートを共有する必要はありません。
 * ・利用者は「メンバー」シートに登録されたGoogleアカウントだけです。
 */

const TZ = 'Asia/Tokyo';
const SH = { CONFIG: '設定', MEMBERS: 'メンバー', HOLIDAYS: '休日', ENTRIES: '申請', COMMENTS: 'コメント', AVG: '日中見込み', LOG: '操作ログ' };
const HEAD = {
  '設定': ['項目', '値', '説明'],
  'メンバー': ['メールアドレス', '氏名', '役割', '有効'],
  '休日': ['日付', '名称'],
  '申請': ['ID', 'メールアドレス', '氏名', '種別', '日付', '開始', '終了', '時間', '振替公休日', '案件', '理由', '状態', '申請日時', '承認者', '承認日時', '作成日時', '更新日時'],
  'コメント': ['ID', '対象者メール', '対象日', '投稿者メール', '投稿者名', 'マネージャー', '本文', '投稿日時'],
  '日中見込み': ['年月', 'メールアドレス', '1日あたり(h)', '入力日時'],
  '操作ログ': ['日時', '実行者', '操作', '対象ID', '内容']
};
const STATUS = { draft: '下書き', pending: '申請中', approved: '承認済', rejected: '差し戻し' };
const KIND = { night: '深夜作業', holiday: '休日出勤' };
// 休日出勤の理由として認めない言い回し（Index.html と同じ）
const NG = /作業したい|進めたい|やりたい|片付けたい|終わらせたい|自主的|作業のため$|作業するため$|特になし|^なし$/;

const DEFAULTS = [
  ['TEAM_NAME', '営業開発部', '画面に表示するチーム名'],
  ['LIMIT_M', 40, '社内基準：月の残業（h）'],
  ['LAW_M', 45, '36協定の原則上限（h）'],
  ['LIMIT_W', 10, '週の目安（h）'],
  ['MIN_FURI', 6, 'この時間以上の休日出勤は振替公休が必要（h）'],
  ['STD', 8, '所定労働時間（h）'],
  ['STREAK', 7, '連続勤務の警告（日）'],
  ['LOCK_DAY', 5, '前月を締める日。この日から前月の申請・承認は変更できない（それまでは前月分も承認できる）'],
  ['SLACK_WEBHOOK_URL', '', 'Slackの通知先（Incoming WebhookのURL）。空なら通知しない'],
  ['APP_URL', '', 'WebアプリのURL（デプロイ後に貼る。通知に載せる）']
];

// 祝日（内閣府の発表で確認してください）。年末年始などの会社休日もこのシートに追加できます。
const HOLIDAYS_SEED = [
  ['2026-01-01', '元日'], ['2026-01-12', '成人の日'], ['2026-02-11', '建国記念の日'], ['2026-02-23', '天皇誕生日'],
  ['2026-03-20', '春分の日'], ['2026-04-29', '昭和の日'], ['2026-05-03', '憲法記念日'], ['2026-05-04', 'みどりの日'],
  ['2026-05-05', 'こどもの日'], ['2026-05-06', '振替休日'], ['2026-07-20', '海の日'], ['2026-08-11', '山の日'],
  ['2026-09-21', '敬老の日'], ['2026-09-22', '国民の休日'], ['2026-09-23', '秋分の日'], ['2026-10-12', 'スポーツの日'],
  ['2026-11-03', '文化の日'], ['2026-11-23', '勤労感謝の日'],
  ['2027-01-01', '元日'], ['2027-01-11', '成人の日'], ['2027-02-11', '建国記念の日'], ['2027-02-23', '天皇誕生日'],
  ['2027-03-21', '春分の日'], ['2027-03-22', '振替休日'], ['2027-04-29', '昭和の日'], ['2027-05-03', '憲法記念日'],
  ['2027-05-04', 'みどりの日'], ['2027-05-05', 'こどもの日'], ['2027-07-19', '海の日'], ['2027-08-11', '山の日'],
  ['2027-09-20', '敬老の日'], ['2027-09-23', '秋分の日'], ['2027-10-11', 'スポーツの日'], ['2027-11-03', '文化の日'],
  ['2027-11-23', '勤労感謝の日']
];

/* ============ 初期設定（最初に1回だけエディタから実行） ============ */

function setup() {
  const ss = SpreadsheetApp.getActive();
  Object.keys(HEAD).forEach(name => {
    const s = ss.getSheetByName(name) || ss.insertSheet(name);
    if (s.getLastRow() === 0) {
      s.getRange(1, 1, 1, HEAD[name].length).setValues([HEAD[name]]).setFontWeight('bold');
      s.setFrozenRows(1);
      // 日付が自動で日付型に変わらないよう、データ行は書式なしテキストにする
      s.getRange(2, 1, s.getMaxRows() - 1, HEAD[name].length).setNumberFormat('@');
    }
  });
  if (sh_(SH.CONFIG).getLastRow() === 1) DEFAULTS.forEach(r => append_(SH.CONFIG, r));
  if (sh_(SH.HOLIDAYS).getLastRow() === 1) HOLIDAYS_SEED.forEach(r => append_(SH.HOLIDAYS, r));
  if (sh_(SH.MEMBERS).getLastRow() === 1) {
    append_(SH.MEMBERS, [Session.getActiveUser().getEmail(), '（氏名を入力）', 'マネージャー', 'TRUE']);
  }
  ['シート1', 'Sheet1'].forEach(n => {
    const s = ss.getSheetByName(n);
    if (s && s.getLastRow() === 0 && ss.getSheets().length > 1) ss.deleteSheet(s);
  });
  Logger.log('初期設定が完了しました。「メンバー」シートにメンバーを登録してください。');
}

/** 毎朝9時の通知（承認待ちの件数、月初と15日の見込み入力の案内）を登録する。エディタから1回実行 */
function installTriggers() {
  ScriptApp.getProjectTriggers().filter(t => t.getHandlerFunction() === 'dailyJob').forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('dailyJob').timeBased().everyDays(1).atHour(9).inTimezone(TZ).create();
}

function dailyJob() {
  const day = Number(Utilities.formatDate(new Date(), TZ, 'd'));
  const wd = Number(Utilities.formatDate(new Date(), TZ, 'u')); // 1=月 … 7=日
  if (day === 1) notify_('🗓 今月の「1日あたりの日中残業の見込み」を入力してください。');
  if (day === 15) notify_('🔁 月の半ばです。日中残業の見込みがずれていたら見直してください。');
  if (wd <= 5) {
    const pending = rows_(SH.ENTRIES).filter(r => r['状態'] === STATUS.pending).length;
    if (pending) notify_(`⏳ 承認待ちの申請が ${pending} 件あります。`);
  }
}

/* ============ Webアプリ ============ */

function doGet() {
  return HtmlService.createTemplateFromFile('Index').evaluate()
    .setTitle('深夜・休日出勤カレンダー')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/** 画面の表示に必要なデータ一式 */
function getData() {
  return build_(ctx_());
}

function saveEntry(p) {
  return mutate_(ctx => {
    const cfg = config_(), hol = holidays_();
    const d = String(p.date || '');
    if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) throw err_('日付が正しくありません');
    if (locked_(d)) throw err_('締め済みの月には追加できません');
    const project = String(p.project || '').trim(), reason = String(p.reason || '').trim();
    if (!project) throw err_('案件・作業を入力してください');
    const e = { id: Utilities.getUuid(), email: ctx.email, date: d, project, reason, status: 'draft', created: now_() };
    if (p.kind === 'holiday') {
      if (!isOff_(d, hol)) throw err_('休日出勤は公休日にだけ登録できます');
      const h = Number(p.hours);
      if (!(h > 0 && h <= 16)) throw err_('実働時間が正しくありません');
      const rc = reasonCheck_(reason);
      if (rc) throw err_(rc);
      e.kind = 'holiday'; e.hours = h; e.furikae = null;
      if (h >= cfg.MIN_FURI) {
        const f = String(p.furikae || '');
        if (!f) throw err_(`${cfg.MIN_FURI}h以上の休日出勤は、振替公休日を選んでください`);
        if (f.slice(0, 7) !== d.slice(0, 7)) throw err_('振替公休は同じ月の中で取ってください');
        if (f === d || isOff_(f, hol)) throw err_('振替公休日には出勤日を選んでください');
        const used = rows_(SH.ENTRIES).map(toEntry_)
          .some(x => x.email === ctx.email && x.kind === 'holiday' && x.status !== 'rejected' && x.furikae === f);
        if (used) throw err_('その日はすでに別の振替公休になっています');
        e.furikae = f;
      }
    } else {
      const s = Number(p.start), en = Number(p.end);
      if (!(en > s) || s < 0 || en > 30) throw err_('時間が正しくありません');
      if (!reason) throw err_('日中にできない理由を入力してください');
      e.kind = 'night'; e.start = s; e.end = en;
    }
    append_(SH.ENTRIES, entryRow_(e, ctx.name));
    log_(ctx, '追加', e.id, `${KIND[e.kind]} ${d} ${project}`);
  });
}

function deleteEntry(id) {
  return mutate_(ctx => {
    const { r, e } = own_(ctx, id, 'draft');
    sh_(SH.ENTRIES).deleteRow(r._row);
    log_(ctx, '削除', id, `${KIND[e.kind]} ${e.date}`);
  });
}

function withdrawEntry(id) {
  return mutate_(ctx => {
    const { r, e } = own_(ctx, id, 'pending');
    e.status = 'draft'; e.sent = '';
    setEntry_(r._row, e, ctx.name);
    log_(ctx, '取り下げ', id, `${KIND[e.kind]} ${e.date}`);
  });
}

function redoEntry(id) {
  return mutate_(ctx => {
    const { r, e } = own_(ctx, id, 'rejected');
    e.status = 'draft';
    setEntry_(r._row, e, ctx.name);
    log_(ctx, '下書きに戻す', id, `${KIND[e.kind]} ${e.date}`);
  });
}

function submitDrafts(ids, why, info) {
  return mutate_(ctx => {
    ids = (ids || []).map(String);
    const targets = rows_(SH.ENTRIES).filter(r => ids.indexOf(r['ID']) >= 0).map(r => ({ r, e: toEntry_(r) }));
    if (!targets.length) throw err_('申請する下書きがありません');
    targets.forEach(({ e }) => {
      if (e.email !== ctx.email || e.status !== 'draft') throw err_('申請できない項目が含まれています。画面を再読み込みしてください');
      if (locked_(e.date)) throw err_('締め済みの月の項目は申請できません');
      if (e.kind === 'holiday') {
        const rc = reasonCheck_(e.reason);
        if (rc) throw err_(`${e.date} の休日出勤：${rc}`);
      }
    });
    const t = now_();
    targets.forEach(({ r, e }) => { e.status = 'pending'; e.sent = t; setEntry_(r._row, e, ctx.name); });
    why = String(why || '').trim();
    if (why) addCommentRow_(ctx, ctx.email, targets.map(x => x.e.date).sort()[0], `【基準超えの理由】${why}`);
    log_(ctx, '申請', ids.join(','), `${targets.length}件${why ? ' 理由：' + why : ''}`);
    notify_(`📝 ${ctx.name} さんから深夜作業・休日出勤の申請が ${targets.length} 件あります${info ? `（${info}）` : ''}。`);
  });
}

function approveEntry(id) {
  return mutate_(ctx => {
    const { r, e } = forManager_(ctx, id);
    e.status = 'approved'; e.by = ctx.name; e.at = now_();
    setEntry_(r._row, e, r['氏名']);
    log_(ctx, '承認', id, `${r['氏名']} ${KIND[e.kind]} ${e.date}`);
    notify_(`✅ ${r['氏名']} さんの ${md_(e.date)} ${KIND[e.kind]} を ${ctx.name} さんが承認しました。`);
  });
}

function rejectEntry(id, text) {
  return mutate_(ctx => {
    text = String(text || '').trim();
    if (!text) throw err_('差し戻しの理由を書いてください');
    const { r, e } = forManager_(ctx, id);
    e.status = 'rejected';
    setEntry_(r._row, e, r['氏名']);
    addCommentRow_(ctx, e.email, e.date, text);
    log_(ctx, '差し戻し', id, `${r['氏名']} ${KIND[e.kind]} ${e.date} 理由：${text}`);
    notify_(`↩️ ${r['氏名']} さんの ${md_(e.date)} ${KIND[e.kind]} が差し戻されました。理由：${text}`);
  });
}

function addComment(target, date, text) {
  return mutate_(ctx => {
    target = lc_(target); text = String(text || '').trim();
    if (!text) throw err_('コメントを入力してください');
    if (!/^\d{4}-\d{2}-\d{2}$/.test(String(date))) throw err_('日付が正しくありません');
    if (ctx.role !== 'manager' && target !== ctx.email) throw err_('ほかの人の予定にはコメントできません');
    addCommentRow_(ctx, target, String(date), text);
  });
}

function setAvg(ym, v) {
  return mutate_(ctx => {
    ym = String(ym);
    if (!/^\d{4}-\d{2}$/.test(ym)) throw err_('年月が正しくありません');
    if (ym < lockYm_()) throw err_('締め済みの月は変更できません');
    const val = v === '' || v === null ? '' : Number(v);
    if (val !== '' && !(val >= 0 && val <= 8)) throw err_('0〜8時間の範囲で入力してください');
    append_(SH.AVG, [ym, ctx.email, val, now_()]);
    log_(ctx, '日中見込み', ym, String(val));
  });
}

/* ============ 内部処理 ============ */

function build_(ctx) {
  const members = members_();
  const visible = ctx.role === 'manager' ? members : members.filter(m => m.email === ctx.email);
  const emails = {};
  visible.forEach(m => emails[m.email] = true);
  const entries = rows_(SH.ENTRIES).map(toEntry_).filter(e => emails[e.email]);
  const comments = rows_(SH.COMMENTS).filter(r => emails[lc_(r['対象者メール'])]).map(r => ({
    id: r['ID'], target: lc_(r['対象者メール']), date: r['対象日'], who: r['投稿者名'],
    mgr: r['マネージャー'] === 'TRUE', text: r['本文'], at: r['投稿日時']
  }));
  const latest = {};
  rows_(SH.AVG).forEach(r => {
    const email = lc_(r['メールアドレス']);
    if (!emails[email]) return;
    latest[email + '|' + r['年月']] = { email, ym: r['年月'], value: r['1日あたり(h)'] === '' ? null : Number(r['1日あたり(h)']), at: r['入力日時'] };
  });
  return {
    me: ctx, today: today_(), lockYm: lockYm_(), config: config_(), holidays: holidays_(),
    members: visible, entries, comments, avg: Object.keys(latest).map(k => latest[k])
  };
}

function mutate_(fn) {
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const ctx = ctx_();
    fn(ctx);
    SpreadsheetApp.flush();
    return build_(ctx);
  } finally {
    lock.releaseLock();
  }
}

function ctx_() {
  const email = lc_(Session.getActiveUser().getEmail());
  if (!email) throw err_('ログイン中のGoogleアカウントを確認できません。会社のアカウントで開いてください。');
  const me = members_().filter(m => m.email === email)[0];
  if (!me) throw err_(`${email} はメンバーに登録されていません。マネージャーに登録を依頼してください。`);
  return me;
}

function members_() {
  return rows_(SH.MEMBERS)
    .filter(r => r['メールアドレス'] && String(r['有効']).toUpperCase() !== 'FALSE')
    .map(r => ({
      email: lc_(r['メールアドレス']),
      name: r['氏名'] || r['メールアドレス'],
      role: /マネージャー|manager/i.test(r['役割']) ? 'manager' : 'member'
    }));
}

function config_() {
  const c = {};
  DEFAULTS.forEach(([k, v]) => c[k] = v);
  rows_(SH.CONFIG).forEach(r => {
    const v = r['値'];
    c[r['項目']] = v !== '' && !isNaN(Number(v)) ? Number(v) : v;
  });
  return c;
}

function holidays_() {
  const h = {};
  rows_(SH.HOLIDAYS).forEach(r => { if (r['日付']) h[r['日付']] = r['名称'] || '休日'; });
  return h;
}

function own_(ctx, id, status) {
  const r = rows_(SH.ENTRIES).filter(x => x['ID'] === String(id))[0];
  if (!r) throw err_('申請が見つかりません。画面を再読み込みしてください');
  const e = toEntry_(r);
  if (e.email !== ctx.email) throw err_('自分の申請だけ操作できます');
  if (e.status !== status) throw err_('この申請は状態が変わっています。画面を再読み込みしてください');
  if (locked_(e.date)) throw err_('締め済みの月の申請は変更できません');
  return { r, e };
}

function forManager_(ctx, id) {
  if (ctx.role !== 'manager') throw err_('承認・差し戻しはマネージャーだけができます');
  const r = rows_(SH.ENTRIES).filter(x => x['ID'] === String(id))[0];
  if (!r) throw err_('申請が見つかりません。画面を再読み込みしてください');
  const e = toEntry_(r);
  if (e.email === ctx.email) throw err_('自分の申請は承認・差し戻しできません');
  if (e.status !== 'pending') throw err_('この申請は承認待ちではありません。画面を再読み込みしてください');
  if (locked_(e.date)) throw err_('締め済みの月の申請は変更できません');
  return { r, e };
}

function toEntry_(r) {
  const status = Object.keys(STATUS).filter(k => STATUS[k] === r['状態'])[0] || 'draft';
  return {
    id: r['ID'], email: lc_(r['メールアドレス']), kind: r['種別'] === KIND.holiday ? 'holiday' : 'night',
    date: r['日付'], start: hnum_(r['開始']), end: hnum_(r['終了']), hours: Number(r['時間']) || 0,
    furikae: r['振替公休日'] || null, project: r['案件'], reason: r['理由'], status,
    sent: r['申請日時'], by: r['承認者'], at: r['承認日時'], created: r['作成日時']
  };
}

function entryRow_(e, name) {
  const night = e.kind === 'night';
  return [e.id, e.email, name, KIND[e.kind], e.date,
    night ? hstr_(e.start) : '', night ? hstr_(e.end) : '', night ? e.end - e.start : e.hours,
    e.furikae || '', e.project, e.reason, STATUS[e.status], e.sent || '', e.by || '', e.at || '', e.created || '', now_()];
}

function setEntry_(row, e, name) {
  const v = entryRow_(e, name).map(x => x === null || x === undefined ? '' : String(x));
  sh_(SH.ENTRIES).getRange(row, 1, 1, v.length).setNumberFormat('@').setValues([v]);
}

function addCommentRow_(ctx, target, date, text) {
  append_(SH.COMMENTS, [Utilities.getUuid(), target, date, ctx.email, ctx.name, ctx.role === 'manager' ? 'TRUE' : 'FALSE', text, now_()]);
}

function reasonCheck_(t) {
  if (!t) return '理由を書いてください';
  if (t.length < 8 || NG.test(t)) return '「作業したいので」などの理由は認められません。顧客都合・イベント当日・障害対応など、休日でなければならない理由を書いてください';
  return '';
}

function notify_(text) {
  const cfg = config_();
  if (!cfg.SLACK_WEBHOOK_URL) return;
  const body = text + (cfg.APP_URL ? `\n${cfg.APP_URL}` : '');
  try {
    UrlFetchApp.fetch(String(cfg.SLACK_WEBHOOK_URL), {
      method: 'post', contentType: 'application/json', payload: JSON.stringify({ text: body }), muteHttpExceptions: true
    });
  } catch (e) {
    console.warn('Slack通知に失敗しました: ' + e);
  }
}

function log_(ctx, op, id, detail) {
  append_(SH.LOG, [now_(), ctx.email, op, id, detail]);
}

/* ---- シート操作 ---- */

function sh_(name) {
  const s = SpreadsheetApp.getActive().getSheetByName(name);
  if (!s) throw err_(`「${name}」シートがありません。setup を実行してください`);
  return s;
}

function rows_(name) {
  const s = sh_(name), last = s.getLastRow(), head = HEAD[name];
  if (last < 2) return [];
  return s.getRange(2, 1, last - 1, head.length).getValues()
    .map((row, i) => {
      const o = { _row: i + 2 };
      head.forEach((k, j) => o[k] = norm_(k, row[j]));
      return o;
    })
    .filter(o => head.some(k => o[k] !== ''));
}

function append_(name, arr) {
  const s = sh_(name), row = s.getLastRow() + 1;
  const v = arr.map(x => x === null || x === undefined ? '' : String(x));
  s.getRange(row, 1, 1, v.length).setNumberFormat('@').setValues([v]);
}

// 人が手で入力して日付型などに変わったセルも、文字列にそろえる
function norm_(k, x) {
  if (x instanceof Date) {
    if (k === '年月') return Utilities.formatDate(x, TZ, 'yyyy-MM');
    if (/日付|対象日|振替公休日/.test(k)) return Utilities.formatDate(x, TZ, 'yyyy-MM-dd');
    if (k === '開始' || k === '終了') return Utilities.formatDate(x, TZ, 'H:mm');
    return Utilities.formatDate(x, TZ, 'yyyy-MM-dd HH:mm');
  }
  if (typeof x === 'boolean') return x ? 'TRUE' : 'FALSE';
  return x === null || x === undefined ? '' : String(x).trim();
}

/* ---- 小物 ---- */

function err_(m) { return new Error(m); }
function lc_(s) { return String(s || '').trim().toLowerCase(); }
function now_() { return Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd HH:mm'); }
function today_() { return Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd'); }
function curYm_() { return today_().slice(0, 7); }
// 締め済みの月：毎月 LOCK_DAY 日になったら前月を締める（月末の申請を月初に承認できるように）
function lockYm_() {
  const t = today_(), cur = t.slice(0, 7), lockDay = Number(config_().LOCK_DAY) || 1;
  if (Number(t.slice(8, 10)) >= lockDay) return cur;
  const p = cur.split('-').map(Number), d = new Date(p[0], p[1] - 2, 1);
  return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2);
}
function locked_(date) { return String(date).slice(0, 7) < lockYm_(); }
function md_(d) { const p = String(d).split('-'); return `${Number(p[1])}/${Number(p[2])}`; }
function isOff_(d, hol) {
  const w = new Date(d + 'T12:00:00+09:00').getUTCDay();
  return w === 0 || w === 6 || !!hol[d];
}
function hnum_(s) {
  if (s === '' || s === null || s === undefined) return null;
  const m = String(s).match(/^(\d+):(\d{2})$/);
  return m ? Number(m[1]) + Number(m[2]) / 60 : Number(s);
}
function hstr_(h) { return Math.floor(h) + ':' + ('0' + Math.round((h % 1) * 60)).slice(-2); }
