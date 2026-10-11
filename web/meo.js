// Mèo Bơ: vẽ bằng SVG, mỗi bộ phận một id/class để meo.css cho chuyển động riêng.
// Cảm xúc/hành động vẫn do app.js đặt lên #face (data-e="vui", class "a-gat_dau"...), file này chỉ lo "cơ thể":
// vẽ mèo, chớp mắt ngẫu nhiên, thỉnh thoảng ngáp/liếm chân/rửa mặt/ngó quanh, vươn vai khi thức dậy, ngoe nguẩy đuôi lúc chờ.
const MEO_SVG = `
<svg class="meo" viewBox="0 0 200 192" aria-hidden="true" focusable="false">
  <defs>
    <clipPath id="meoClipDau"><ellipse cx="100" cy="74" rx="58" ry="47"/></clipPath>
    <clipPath id="meoClipThan"><ellipse cx="100" cy="130" rx="68" ry="50"/></clipPath>
  </defs>
  <g id="meoTail" class="tail">
    <path class="vien" d="M150,152 C186,150 194,110 184,84 C179,72 168,72 170,86"/>
    <path class="long" d="M150,152 C186,150 194,110 184,84 C179,72 168,72 170,86"/>
  </g>
  <g id="meoBody" class="body">
    <ellipse class="da" cx="100" cy="130" rx="68" ry="50"/>
    <g class="dom" clip-path="url(#meoClipThan)"><ellipse class="dom-den" cx="50" cy="110" rx="28" ry="22"/><ellipse class="dom-cam" cx="152" cy="142" rx="26" ry="28"/></g>
    <ellipse class="vien-dom" cx="100" cy="130" rx="68" ry="50"/>
    <ellipse class="bung" cx="100" cy="140" rx="40" ry="32"/>
    <path class="soc" d="M38,118 Q46,122 44,132 M36,138 Q44,140 42,150 M162,118 Q154,122 156,132 M164,138 Q156,140 158,150"/>
    <path class="soc van-them" d="M48,100 Q56,104 54,114 M152,100 Q144,104 146,114 M40,156 Q48,158 48,166 M160,156 Q152,158 152,166"/>
    <path class="long-dung" d="M62,91 L57,82 M51,98 L44,90 M42,107 L34,101 M36,117 L27,113 M34,128 L24,127 M35,138 L25,141 M39,149 L30,154 M46,158 L39,165 M138,91 L143,82 M149,98 L156,90 M158,107 L166,101 M164,117 L173,113 M166,128 L176,127 M165,138 L175,141 M161,149 L170,154 M154,158 L161,165"/>
  </g>
  <ellipse class="da chan-sau" cx="50" cy="170" rx="22" ry="12"/>
  <ellipse class="da chan-sau" cx="150" cy="170" rx="22" ry="12"/>
  <g id="meoHead" class="head">
    <g id="meoEarL" class="ear ear-l"><path class="da" d="M52,58 Q38,16 50,10 Q60,8 92,32 Z"/><path class="tai-trong" d="M57,48 Q50,24 55,20 Q62,18 80,33 Z"/></g>
    <g id="meoEarR" class="ear ear-r"><path class="da" d="M148,58 Q162,16 150,10 Q140,8 108,32 Z"/><path class="tai-trong" d="M143,48 Q150,24 145,20 Q138,18 120,33 Z"/></g>
    <ellipse class="da" cx="100" cy="74" rx="58" ry="47"/>
    <g class="dom" clip-path="url(#meoClipDau)"><ellipse class="dom-cam" cx="62" cy="48" rx="30" ry="26"/><ellipse class="dom-den" cx="142" cy="42" rx="26" ry="22"/></g>
    <ellipse class="vien-dom" cx="100" cy="74" rx="58" ry="47"/>
    <path class="soc van-them" d="M43,68 L55,71 M43,77 L54,78 M157,68 L145,71 M157,77 L146,78 M94,30 L95,38 M106,30 L105,38"/>
    <path class="soc" d="M100,29 L100,40 M87,31 L90,41 M113,31 L110,41"/>
    <ellipse class="ma" cx="64" cy="90" rx="9" ry="5"/><ellipse class="ma" cx="136" cy="90" rx="9" ry="5"/>
    <g class="mat">
      <g class="mat-mo"><g class="nhin">
        <ellipse class="den" cx="78" cy="74" rx="8" ry="10"/><ellipse class="den" cx="122" cy="74" rx="8" ry="10"/>
        <ellipse class="dong-tu" cx="78" cy="74" rx="2.6" ry="7.5"/><ellipse class="dong-tu" cx="122" cy="74" rx="2.6" ry="7.5"/>
        <g class="con-nguoi"><circle class="sang" cx="81" cy="70" r="3"/><circle class="sang" cx="125" cy="70" r="3"/></g>
      </g></g>
      <path class="mat-cuoi net" d="M70,77 Q78,66 86,77 M114,77 Q122,66 130,77"/>
      <path class="mat-nham net" d="M70,74 Q78,81 86,74 M114,74 Q122,81 130,74"/>
      <path class="mat-xoay" d="M78.0,74.0 L78.2,74.1 L78.3,74.5 L78.0,74.8 L77.6,75.0 L77.1,74.8 L76.6,74.2 L76.5,73.3 L76.8,72.4 L77.6,71.6 L78.7,71.4 L79.8,71.9 L80.7,73.1 L81.0,74.8 L80.5,76.5 L79.2,77.8 L77.5,78.3 L75.6,77.7 L74.1,76.0 L73.5,73.6 L74.1,71.1 L75.7,69.0 L78.0,68.1 L80.6,68.6 L82.8,70.5 L83.9,73.6 L83.5,77.0 L81.8,79.9 L78.9,81.5 L75.6,81.3 L72.6,79.3 L70.9,75.7 L70.8,71.5 L72.6,67.7 L75.8,65.2 L79.8,64.8 M122.0,74.0 L122.2,74.1 L122.3,74.5 L122.0,74.8 L121.6,75.0 L121.1,74.8 L120.6,74.2 L120.5,73.3 L120.8,72.4 L121.6,71.6 L122.7,71.4 L123.8,71.9 L124.7,73.1 L125.0,74.8 L124.5,76.5 L123.2,77.8 L121.5,78.3 L119.6,77.7 L118.1,76.0 L117.5,73.6 L118.1,71.1 L119.7,69.0 L122.0,68.1 L124.6,68.6 L126.8,70.5 L127.9,73.6 L127.5,77.0 L125.8,79.9 L122.9,81.5 L119.6,81.3 L116.6,79.3 L114.9,75.7 L114.8,71.5 L116.6,67.7 L119.8,65.2 L123.8,64.8"/>
    </g>
    <path class="mui" d="M95,85 L105,85 L100,91 Z"/>
    <path class="mieng mieng-w net" d="M100,91 L100,93 M90,93 Q95,99 100,93 Q105,99 110,93"/>
    <path class="mieng mieng-buon net" d="M91,100 Q100,92 109,100"/>
    <g class="mieng mieng-mo"><ellipse class="trong-mieng" cx="100" cy="98" rx="8" ry="7"/><ellipse class="luoi" cx="100" cy="102" rx="5" ry="3"/></g>
    <path class="luoi-liem" d="M96,94 Q100,104 104,94 Z"/>
    <path class="ria" d="M62,88 L28,82 M62,94 L26,96 M138,88 L172,82 M138,94 L174,96"/>
  </g>
  <g id="meoPawL" class="paw paw-l">
    <ellipse class="da" cx="82" cy="174" rx="14" ry="10"/>
    <path class="ngon" d="M77,178 L77,182 M87,178 L87,182"/>
  </g>
  <g id="meoPawR" class="paw paw-r">
    <ellipse class="da" cx="118" cy="174" rx="14" ry="10"/>
    <path class="ngon" d="M113,178 L113,182 M123,178 L123,182"/>
  </g>
  <g class="tail-ngu">
    <path class="vien" d="M152,166 C154,192 70,194 58,178"/>
    <path class="long" d="M152,166 C154,192 70,194 58,178"/>
  </g>
  <g class="zzz"><text x="150" y="40">z</text><text x="164" y="26">z</text><text x="178" y="12">Z</text></g>
</svg>`;

// Việc vặt lúc rảnh: r là số ngẫu nhiên 0..1. Trả về [tên trạng thái, số ms].
// Khuya hay ngáp; đang nằm bẹp (ổ bánh mì, giấu chân) thì không liếm chân/rửa mặt mà chỉ ngáp hoặc ngó quanh.
function boViecVat(r, khuya, bep) {
  let v = khuya ? (r < 0.75 ? 'ngap' : r < 0.88 ? 'liem' : 'ngo')
                : (r < 0.3 ? 'ngap' : r < 0.55 ? 'liem' : r < 0.78 ? 'rua-mat' : 'ngo');
  if (bep && (v === 'liem' || v === 'rua-mat')) v = 'ngo';
  return [v, { ngap: 2200, liem: 2600, 'rua-mat': 3200, ngo: 2600 }[v]];
}
if (typeof module !== 'undefined') module.exports = { boViecVat };

(function () {
  if (typeof document === 'undefined') return;
  const face = document.getElementById('face');
  if (!face) return;
  face.innerHTML = MEO_SVG;
  // Kiểu lông đã chọn (hop_thoai.js cho chọn): thuong / van (mướp vằn) / tam_the / den
  try { const l = localStorage.getItem('bo_long'); if (l && /^(van|tam_the|den)$/.test(l)) face.dataset.long = l; } catch (e) {}
  const svg = face.querySelector('svg');
  const yenLang = () => window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  const dangNgu = () => face.dataset.e === 'ngu';
  // Bật một trạng thái ngắn trên mèo (chớp mắt, ngáp...) rồi tự tắt
  function lan(cls, ms) {
    svg.classList.add(cls);
    setTimeout(() => svg.classList.remove(cls), ms);
  }
  // Chớp mắt ngẫu nhiên (không theo nhịp đều cho giống thật), thỉnh thoảng chớp hai cái liền
  function chopMat() {
    if (!dangNgu() && !document.hidden) {
      lan('chop', 150);
      if (Math.random() < 0.2) setTimeout(() => lan('chop', 150), 300);
    }
    setTimeout(chopMat, 2200 + Math.random() * 4500);
  }
  setTimeout(chopMat, 1500);
  // Thỉnh thoảng ngáp hoặc liếm chân khi rảnh (không lúc đang nói, đang ngủ, đang chờ trả lời)
  // Khuya (22h–5h): Bơ buồn ngủ — mắt lim dim, ngáp nhiều hơn, ít liếm chân
  const khuya = () => { const h = new Date().getHours(); return h >= 22 || h < 5; };
  function capNhatKhuya() { svg.classList.toggle('lim-dim', khuya()); }
  capNhatKhuya(); setInterval(capNhatKhuya, 60000);
  function viecVat() {
    const ban = dangNgu() || face.classList.contains('talking') || svg.classList.contains('cho') || document.hidden;
    const k = khuya();
    if (!ban && !yenLang()) lan(...boViecVat(Math.random(), k, svg.classList.contains('bep')));
    setTimeout(viecVat, (k ? 15000 : 25000) + Math.random() * (k ? 15000 : 30000));
  }
  setTimeout(viecVat, 20000);
  // Ngủ say: thỉnh thoảng giật tai trong mơ hoặc trở mình một cái
  function mo() {
    if (dangNgu() && !document.hidden && !yenLang()) {
      const r = Math.random();
      lan(r < 0.4 ? 'giat-tai-trai' : r < 0.7 ? 'giat-tai-phai' : 'tro-minh', r < 0.7 ? 450 : 1400);
    }
    setTimeout(mo, 12000 + Math.random() * 20000);
  }
  setTimeout(mo, 15000);
  // Thức dậy sau giấc ngủ gật: vươn vai một cái
  let truoc = face.dataset.e;
  new MutationObserver(() => {
    const nay = face.dataset.e;
    if (truoc === 'ngu' && nay !== 'ngu') lan('vuon', 1300);
    truoc = nay;
  }).observe(face, { attributes: true, attributeFilter: ['data-e'] });
  // app.js gọi meo.cho(true) khi Bơ đang nghĩ/gõ: mèo ngoe nguẩy đuôi, nhìn lên; meo.dat('nghe', true) khi micro đang nghe
  window.meo = { cho(bat) { svg.classList.toggle('cho', !!bat); }, dat(cls, bat) { svg.classList.toggle(cls, !!bat); }, lan };
})();
