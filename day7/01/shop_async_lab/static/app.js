const names = {sync: '동기 · 순차 조회', blocking: '이벤트 루프 차단', async: '비동기 · 동시 조회', thread: '기존 동기 코드 개선'};
const explanations = {
  sync: '동기 함수가 상품 → 재고 → 배송을 순서대로 조회합니다. 전체 작업은 스레드에서 실행하므로, 조회는 느려도 서버는 다른 요청에 응답할 수 있습니다.',
  blocking: 'asyncio.gather로 묶어도 내부의 time.sleep이 이벤트 루프를 막습니다. 조회가 순서대로 실행되고 같은 서버의 다른 요청도 기다립니다. 학습용으로 의도한 잘못된 구현입니다.',
  async: 'asyncio.gather로 세 작업을 함께 시작합니다. await asyncio.sleep으로 I/O 대기 중 실행권을 양보하여 다른 조회와 요청을 처리합니다.',
  thread: '기존 동기 함수의 time.sleep은 유지하고, asyncio.to_thread로 각각 별도 스레드에서 실행합니다. 이벤트 루프를 막지 않고 함께 기다립니다.'
};
const $ = id => document.getElementById(id);
let mode = 'sync', busy = false, history = [];
$('explanation').textContent = explanations[mode];
function selectMode(next) {
  mode = next;
  document.querySelectorAll('.mode').forEach(button => {
    button.classList.toggle('active', button.dataset.mode === mode);
    button.setAttribute('aria-pressed', String(button.dataset.mode === mode));
  });
  $('explanation').textContent = explanations[mode];
}
document.querySelectorAll('.mode').forEach(button => button.addEventListener('click', () => selectMode(button.dataset.mode)));
function lock(value) {
  busy = value;
  document.querySelectorAll('.mode, #run, #compare, #scale').forEach(el => el.disabled = value);
}
async function getJSON(url) {
  const response = await fetch(url, {cache: 'no-store', signal: AbortSignal.timeout(90000)});
  if (!response.ok) throw new Error(`서버 응답 오류 (${response.status})`);
  return response.json();
}
async function checkHealth() {
  const start = performance.now();
  await getJSON('/api/health');
  return performance.now() - start;
}
function render(data, latency) {
  $('elapsed').innerHTML = `${data.elapsed.toFixed(2)} <small>초</small>`;
  $('latency').innerHTML = `${Math.round(latency)} <small>ms</small>`;
  const total = Math.max(data.elapsed, ...data.results.map(result => result.end));
  $('timeline').innerHTML = data.results.map(result => `<div class="track"><span>${result.label}</span><div class="track-space"><div class="bar" style="left:${result.start / total * 100}%;width:${(result.end - result.start) / total * 100}%"></div></div><time>${result.start.toFixed(2)}–${result.end.toFixed(2)}초</time></div>`).join('') + `<div class="axis"><span>0초</span><span>${total.toFixed(2)}초</span></div>`;
  $('service-results').innerHTML = data.results.map(result => `<div class="service"><strong>✓ ${result.label}</strong>${result.value}</div>`).join('');
  history.unshift({data, latency});
  history = history.slice(0, 20);
  $('history').innerHTML = history.map(({data, latency}) => `<tr><td>${names[data.mode]}</td>${data.results.map(result => `<td>${(result.end - result.start).toFixed(2)}초</td>`).join('')}<td><strong>${data.elapsed.toFixed(2)}초</strong></td><td>${Math.round(latency)} ms</td></tr>`).join('');
}
async function runOne(selected) {
  selectMode(selected);
  $('elapsed').innerHTML = '… <small>초</small>';
  $('latency').innerHTML = '… <small>ms</small>';
  $('timeline').innerHTML = '<p class="empty">조회 중입니다. 완료 후 실제 서버 시간표가 표시됩니다.</p>';
  $('service-results').replaceChildren();
  const started = performance.now();
  const timer = setInterval(() => {
    $('status').textContent = `${names[selected]} 진행 중 · ${((performance.now() - started) / 1000).toFixed(1)}초 경과`;
  }, 100);
  try {
    // 타이머를 예약하면서 조회 요청도 즉시 시작한다. 완료를 기다렸다 health를 보내지 않는다.
    const healthPromise = new Promise(resolve => setTimeout(resolve, 150)).then(checkHealth);
    const checkoutPromise = getJSON(`/api/checkout/${selected}?scale=${$('scale').value}`);
    const [checkout, health] = await Promise.allSettled([checkoutPromise, healthPromise]);
    if (checkout.status === 'rejected') throw checkout.reason;
    if (health.status === 'rejected') throw health.reason;
    render(checkout.value, health.value);
    $('status').textContent = `${names[selected]} 완료 · ${checkout.value.elapsed.toFixed(2)}초 / 서버 응답 대기 ${Math.round(health.value)}ms`;
  } finally { clearInterval(timer); }
}
async function run(all) {
  if (busy) return;
  lock(true);
  $('status').classList.remove('error');
  try {
    for (const selected of all ? Object.keys(names) : [mode]) await runOne(selected);
    if (all) $('status').textContent = '4가지 비교 완료 · 아래 실행 기록에서 전체 시간과 서버 응답 대기를 비교해 보세요.';
  } catch (error) {
    $('status').classList.add('error');
    $('status').textContent = `조회 실패: ${error.message}. 서버 실행 상태를 확인하고 다시 시도하세요.`;
    $('elapsed').textContent = '실패';
    $('latency').textContent = '—';
    $('timeline').innerHTML = '<p class="empty">조회에 실패하여 시간표를 표시할 수 없습니다.</p>';
  } finally { lock(false); }
}
$('run').addEventListener('click', () => run(false));
$('compare').addEventListener('click', () => run(true));
$('health').addEventListener('click', async () => {
  $('health').disabled = true;
  $('health-note').textContent = '별도 서버 응답을 기다리는 중…';
  try { $('health-note').textContent = `수동 확인: ${Math.round(await checkHealth())}ms 만에 응답했습니다. 상단 측정값은 조회 중 자동 확인 결과입니다.`; }
  catch (error) { $('health-note').textContent = `응답 확인 실패: ${error.message}`; }
  finally { $('health').disabled = false; }
});
