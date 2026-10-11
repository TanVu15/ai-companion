// Mèo Bơ: vẽ bằng SVG, mỗi bộ phận một id/class để meo.css cho chuyển động riêng.
// Cảm xúc/hành động vẫn do app.js đặt lên #face (data-e="vui", class "a-gat_dau"...), file này chỉ lo "cơ thể":
// vẽ mèo, chớp mắt ngẫu nhiên, thỉnh thoảng ngáp/liếm chân, vươn vai khi thức dậy, ngoe nguẩy đuôi lúc chờ.
const MEO_SVG = `
<svg class="meo" viewBox="0 0 200 192" aria-hidden="true" focusable="false">
  <g id="meoTail" class="tail">
    <path class="vien" d="M150,152 C186,150 194,110 184,84 C179,72 168,72 170,86"/>
    <path class="long" d="M150,152 C186,150 194,110 184,84 C179,72 168,72 170,86"/>
  </g>
  <g id="meoBody" class="body">
    <ellipse class="da" cx="100" cy="130" rx="68" ry="50"/>
    <ellipse class="bung" cx="100" cy="140" rx="40" ry="32"/>
    <path class="soc" d="M38,118 Q46,122 44,132 M36,138 Q44,140 42,150 M162,118 Q154,122 156,132 M164,138 Q156,140 158,150"/>
  </g>
  <ellipse class="da chan-sau" cx="50" cy="170" rx="22" ry="12"/>
  <ellipse class="da chan-sau" cx="150" cy="170" rx="22" ry="12"/>
  <g id="meoHead" class="head">
    <g id="meoEarL" class="ear ear-l"><path class="da" d="M52,58 Q38,16 50,10 Q60,8 92,32 Z"/><path class="tai-trong" d="M57,48 Q50,24 55,20 Q62,18 80,33 Z"/></g>
    <g id="meoEarR" class="ear ear-r"><path class="da" d="M148,58 Q162,16 150,10 Q140,8 108,32 Z"/><path class="tai-trong" d="M143,48 Q150,24 145,20 Q138,18 120,33 Z"/></g>
    <ellipse class="da" cx="100" cy="74" rx="58" ry="47"/>
    <path class="soc" d="M100,29 L100,40 M87,31 L90,41 M113,31 L110,41"/>
    <ellipse class="ma" cx="64" cy="90" rx="9" ry="5"/><ellipse class="ma" cx="136" cy="90" rx="9" ry="5"/>
    <g class="mat">
      <g class="mat-mo">
        <ellipse class="den" cx="78" cy="74" rx="8" ry="10"/><ellipse class="den" cx="122" cy="74" rx="8" ry="10"/>
        <g class="con-nguoi"><circle class="sang" cx="81" cy="70" r="3"/><circle class="sang" cx="125" cy="70" r="3"/></g>
      </g>
      <path class="mat-cuoi net" d="M70,77 Q78,66 86,77 M114,77 Q122,66 130,77"/>
      <path class="mat-nham net" d="M70,74 Q78,81 86,74 M114,74 Q122,81 130,74"/>
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

(function () {
  const face = document.getElementById('face');
  if (!face) return;
  face.innerHTML = MEO_SVG;
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
  function viecVat() {
    const ban = dangNgu() || face.classList.contains('talking') || svg.classList.contains('cho') || document.hidden;
    if (!ban && !yenLang()) Math.random() < 0.5 ? lan('ngap', 2200) : lan('liem', 2600);
    setTimeout(viecVat, 25000 + Math.random() * 30000);
  }
  setTimeout(viecVat, 20000);
  // Thức dậy sau giấc ngủ gật: vươn vai một cái
  let truoc = face.dataset.e;
  new MutationObserver(() => {
    const nay = face.dataset.e;
    if (truoc === 'ngu' && nay !== 'ngu') lan('vuon', 1300);
    truoc = nay;
  }).observe(face, { attributes: true, attributeFilter: ['data-e'] });
  // app.js gọi meo.cho(true) khi Bơ đang nghĩ/gõ: mèo ngoe nguẩy đuôi, nhìn lên
  window.meo = { cho(bat) { svg.classList.toggle('cho', !!bat); }, lan };
})();
