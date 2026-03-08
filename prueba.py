import { useState, useRef } from "react";

const CORPS = {
  canaria: { id: "canaria", name: "Policía Canaria", color: "#FFD700", accent: "#FF6B00", badge: "🛡️", emblem: "GOBIERNO DE CANARIAS" },
  local:   { id: "local",   name: "Policía Local",   color: "#4FC3F7", accent: "#0288D1", badge: "⚖️", emblem: "CABILDO INSULAR" },
};

const DEMO = {
  id: 0, titulo: "Supuesto Demo — Alteración del Orden Público",
  enunciado: "Son las 23:47 horas del sábado 15 de marzo. La Central de Comunicaciones recibe una llamada alertando de una pelea multitudinaria en la Plaza del Mercado. Al llegar a la escena, los agentes encuentran a un grupo de aproximadamente 20 personas involucradas en una reyerta. Hay tres personas lesionadas visibles. Uno de los implicados porta lo que parece ser una botella rota.",
  preguntas: [
    { id:1, texto:"¿Cuál debe ser la primera acción del agente al llegar a la escena?", opciones:["A) Identificar a todos los presentes","B) Evaluar la situación y solicitar refuerzos","C) Proceder a la detención del individuo con la botella","D) Acordonar el perímetro sin intervenir"], correcta:1, explicacion:"La evaluación situacional es prioritaria según el protocolo de actuación policial." },
    { id:2, texto:"Respecto al individuo con la botella rota, el agente debe:", opciones:["A) Ignorarlo hasta controlar al resto","B) Dispararle como medida preventiva","C) Neutralizar la amenaza de forma proporcional","D) Llamar a los servicios médicos antes de intervenir"], correcta:2, explicacion:"El principio de proporcionalidad obliga al agente a identificar y neutralizar la amenaza más grave primero." },
    { id:3, texto:"Las personas lesionadas deben ser atendidas:", opciones:["A) Solo por el agente con primeros auxilios","B) Solicitando asistencia sanitaria al 112","C) Solo tras detener a todos los implicados","D) Por los testigos civiles"], correcta:1, explicacion:"La obligación de socorro es un deber legal y ético. Se debe solicitar asistencia médica inmediata." },
  ],
};

// ─── Persistencia por cuerpo ────────────────────────────
const STORAGE_KEY = (corp) => `academia_supuestos_${corp}`;

const loadSupuestos = (corp) => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY(corp));
    return raw ? JSON.parse(raw) : [];
  } catch { return []; }
};

const saveSupuestos = (corp, list) => {
  try { localStorage.setItem(STORAGE_KEY(corp), JSON.stringify(list)); } catch {}
};

// ─── Marco normativo para el asistente ──────────────────
const MARCO_NORMATIVO = `Marco normativo aplicable (cita siempre artículos concretos):
- Constitución Española (CE): arts. 17 (libertad), 18 (intimidad), 24 (tutela judicial), 25 (legalidad penal).
- Ley Orgánica 2/1986, de Fuerzas y Cuerpos de Seguridad (LOFCS): arts. 5 (principios de actuación), 11 (funciones), 52 y ss. (Policía Local).
- Ley de Enjuiciamiento Criminal (LECrim): arts. 282 (función policial), 292 (atestado), 489-501 (detención).
- Ley Orgánica 4/2015, de Seguridad Ciudadana (LSC): arts. 16-17 (identificación), 19 (entrada y registro), 20 (medidas de seguridad).
- Ley Orgánica 10/1995, Código Penal (CP): arts. 20 (eximentes), 21-23 (atenuantes/agravantes), 163-172 (detenciones ilegales, coacciones), 550-556 (atentado y resistencia a la autoridad).
- Ley 7/1985, de Bases del Régimen Local (LBRL): art. 25 (competencias municipales), 54 (responsabilidad).
- Real Decreto 137/1993, Reglamento de Armas: uso proporcional y reglamentario.
- Ley Orgánica 3/2018, Protección de Datos Personales (LOPDGDD).
- Normativa autonómica canaria: Ley 6/1997 de Coordinación de Policías Locales de Canarias; Decreto 178/2006 de Reglamento Marco de Policías Locales de Canarias.
- Principios generales de actuación policial: legalidad, necesidad, proporcionalidad, oportunidad y congruencia.`;

function LoadingDots() {
  return (
    <span style={{ display:"inline-flex", gap:4, alignItems:"center" }}>
      {[0,1,2].map(i => (
        <span key={i} style={{ width:5, height:5, borderRadius:"50%", background:"currentColor", display:"inline-block",
          animation:`ldot 1.2s ease-in-out ${i*0.2}s infinite` }} />
      ))}
      <style>{`@keyframes ldot{0%,80%,100%{opacity:.25;transform:scale(.7)}40%{opacity:1;transform:scale(1)}}`}</style>
    </span>
  );
}

/* ─── SELECTOR DE CUERPO ─────────────────────────────── */
function CorpSelector({ onSelect }) {
  const [hov, setHov] = useState(null);
  return (
    <div style={{ minHeight:"100vh", background:"#09090f", display:"flex", flexDirection:"column",
      alignItems:"center", justifyContent:"center", fontFamily:"system-ui,sans-serif", padding:"2rem",
      backgroundImage:"radial-gradient(ellipse at 20% 50%,#1a0a0010 0%,transparent 60%),radial-gradient(ellipse at 80% 20%,#00101a10 0%,transparent 60%)" }}>
      <div style={{ textAlign:"center", marginBottom:"3.5rem" }}>
        <div style={{ fontSize:"0.65rem", letterSpacing:"0.4em", color:"#555", marginBottom:"0.8rem", textTransform:"uppercase" }}>Sistema de Entrenamiento</div>
        <h1 style={{ fontSize:"clamp(2rem,5vw,3.2rem)", fontWeight:"700", color:"#f5f0e8", fontFamily:"Georgia,serif",
          letterSpacing:"0.02em", marginBottom:"1rem", textShadow:"0 0 40px rgba(255,200,50,0.2)" }}>
          Academia · Islas Canarias
        </h1>
        <div style={{ width:50, height:2, background:"linear-gradient(90deg,transparent,#FFD700,transparent)", margin:"0 auto 1rem" }} />
        <p style={{ color:"#666", fontSize:"0.9rem" }}>Selecciona tu cuerpo policial para comenzar</p>
      </div>
      <div style={{ display:"flex", gap:"1.5rem", flexWrap:"wrap", justifyContent:"center" }}>
        {Object.values(CORPS).map(corp => (
          <button key={corp.id} onClick={() => onSelect(corp.id)}
            onMouseEnter={() => setHov(corp.id)} onMouseLeave={() => setHov(null)}
            style={{ background: hov===corp.id ? `linear-gradient(135deg,${corp.color}12,${corp.accent}18)` : "rgba(255,255,255,0.025)",
              border:`1px solid ${hov===corp.id ? corp.color : "rgba(255,255,255,0.07)"}`,
              borderRadius:6, padding:"2.5rem 2rem", cursor:"pointer", transition:"all 0.3s",
              display:"flex", flexDirection:"column", alignItems:"center", gap:"1.25rem", minWidth:240,
              boxShadow: hov===corp.id ? `0 16px 50px ${corp.color}18` : "none",
              transform: hov===corp.id ? "translateY(-3px)" : "none" }}>
            <div style={{ fontSize:"2.5rem" }}>{corp.badge}</div>
            <div style={{ textAlign:"center" }}>
              <div style={{ fontSize:"0.6rem", letterSpacing:"0.3em", color:corp.color, opacity:0.7, marginBottom:"0.4rem", textTransform:"uppercase" }}>{corp.emblem}</div>
              <div style={{ fontSize:"1.25rem", fontWeight:"600", color:"#f5f0e8" }}>{corp.name}</div>
            </div>
            <div style={{ fontSize:"0.75rem", color:corp.color, opacity: hov===corp.id?1:0, transition:"opacity 0.2s", letterSpacing:"0.1em", textTransform:"uppercase" }}>
              Entrar →
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

/* ─── BIBLIOTECA ─────────────────────────────────────── */
function Library({ corp, onStartTest, onBack }) {
  const [supuestos, setSupuestos] = useState(() => {
    const saved = loadSupuestos(corp);
    return saved.length > 0 ? saved : [DEMO];
  });
  const [dragOver, setDragOver] = useState(false);
  const [status, setStatus] = useState(null);
  const fileRef = useRef();
  const c = CORPS[corp];

  const addSupuesto = (s) => {
    setSupuestos(prev => {
      const next = [...prev, s];
      saveSupuestos(corp, next);
      return next;
    });
  };

  const deleteSupuesto = (id) => {
    if (!confirm('¿Eliminar este supuesto de la biblioteca?')) return;
    setSupuestos(prev => {
      const next = prev.filter(s => s.id !== id);
      saveSupuestos(corp, next);
      return next;
    });
  };

  const toBase64 = (buf) => {
    const bytes = new Uint8Array(buf);
    let bin = "";
    for (let i = 0; i < bytes.length; i += 8192)
      bin += String.fromCharCode(...bytes.subarray(i, i + 8192));
    return btoa(bin);
  };

  const loadPdfJs = () => new Promise((res, rej) => {
    if (window.pdfjsLib) { res(window.pdfjsLib); return; }
    const s = document.createElement("script");
    s.src = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js";
    s.onload = () => { window.pdfjsLib.GlobalWorkerOptions.workerSrc = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js"; res(window.pdfjsLib); };
    s.onerror = () => rej(new Error("No se pudo cargar pdf.js"));
    document.head.appendChild(s);
  });

  const extractText = async (buf) => {
    const lib = await loadPdfJs();
    const pdf = await lib.getDocument({ data: buf.slice(0) }).promise;
    let text = "";
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const ct = await page.getTextContent();
      text += ct.items.map(it => it.str).join(" ") + "\n";
    }
    return text.trim();
  };

  const callClaude = async (content) => {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method:"POST", headers:{ "Content-Type":"application/json" },
      body: JSON.stringify({ model:"claude-opus-4-5", max_tokens:8000, messages:[{ role:"user", content }] })
    });
    const j = await r.json();
    if (j.error) throw new Error("API: " + j.error.message);
    return j.content?.map(b => b.text||"").join("") || "";
  };

  const PROMPT = `Eres un extractor de exámenes policiales. Extrae TODAS las preguntas del documento sin omitir ninguna.
Devuelve SOLO JSON válido (sin markdown, sin texto extra) con esta estructura:
{"titulo":"...","enunciado":"texto del caso en una sola línea sin saltos de línea reales","preguntas":[{"id":1,"texto":"pregunta sin saltos de línea reales","opciones":["A) ...","B) ...","C) ...","D) ..."],"correcta":0,"explicacion":"explicación sin saltos de línea reales"}]}
REGLAS CRÍTICAS:
- Extrae ABSOLUTAMENTE TODAS las preguntas del documento. Cuenta las preguntas antes de responder y asegúrate de incluirlas todas.
- "correcta" es el índice 0-3 de la respuesta correcta según el documento (0=A, 1=B, 2=C, 3=D).
- NUNCA uses saltos de línea reales dentro de los valores string del JSON. Usa el espacio en su lugar.
- NUNCA uses comillas sin escapar dentro de los strings.
- El JSON resultante debe ser 100% válido y parseable con JSON.parse().`;

  const handleFile = async (file) => {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith(".pdf")) { setStatus({ error:"Solo se aceptan archivos PDF." }); return; }

    try {
      setStatus({ phase:"leyendo", msg:"Leyendo PDF…", progress:15 });
      const buf = await file.arrayBuffer();

      setStatus({ phase:"extrayendo", msg:"Extrayendo texto…", progress:35 });
      let pdfText = "";
      try { pdfText = await extractText(buf); } catch(e) { console.warn("pdf.js:", e.message); }

      setStatus({ phase:"ia", msg:`Analizando con IA${pdfText.length > 80 ? ` (${pdfText.length} caracteres)` : " (PDF completo)"}…`, progress:55 });

      let raw = "";
      if (pdfText.length > 80) {
        raw = await callClaude([{ type:"text", text: PROMPT + "\n\nTEXTO DEL SUPUESTO:\n" + pdfText }]);
      } else {
        raw = await callClaude([
          { type:"document", source:{ type:"base64", media_type:"application/pdf", data: toBase64(buf) } },
          { type:"text", text: PROMPT }
        ]);
      }

      setStatus({ phase:"parseando", msg:"Procesando respuesta…", progress:80 });

      const match = raw.match(/\{[\s\S]*\}/);
      if (!match) throw new Error("La IA no devolvió JSON.\n\nRespuesta:\n" + raw.slice(0,400));

      let parsed;
      try {
        parsed = JSON.parse(match[0]);
      } catch(e1) {
        setStatus({ phase:"reparando", msg:"Reparando JSON…", progress:88 });
        const fixed = await callClaude([{ type:"text",
          text:`Repara este JSON mal formado y devuelve SOLO el JSON corregido, sin texto extra ni backticks. Error: ${e1.message}\n\nJSON:\n${match[0].slice(0,10000)}` }]);
        const fixMatch = fixed.match(/\{[\s\S]*\}/);
        if (!fixMatch) throw new Error("No se pudo reparar el JSON.");
        parsed = JSON.parse(fixMatch[0]);
      }

      if (!parsed.preguntas?.length) throw new Error("No se encontraron preguntas. ¿El PDF tiene formato tipo test?");

      parsed.id = Date.now();
      addSupuesto(parsed);
      setStatus({ phase:"ok", msg:`✓ "${parsed.titulo}" — ${parsed.preguntas.length} preguntas añadidas`, progress:100 });
      setTimeout(() => setStatus(null), 5000);

    } catch(err) {
      console.error(err);
      setStatus({ error: err.message });
    }
  };

  const busy = status?.phase && status.phase !== "ok";

  return (
    <div style={{ minHeight:"100vh", background:"#09090f",
      backgroundImage:`radial-gradient(ellipse at 10% 0%,${c.color}06 0%,transparent 50%)`,
      fontFamily:"system-ui,sans-serif", color:"#f0ece0" }}>

      <div style={{ borderBottom:"1px solid rgba(255,255,255,0.06)", padding:"0.9rem 2rem",
        display:"flex", alignItems:"center", gap:"1rem",
        background:"rgba(0,0,0,0.5)", backdropFilter:"blur(10px)", position:"sticky", top:0, zIndex:10 }}>
        <button onClick={onBack} style={{ background:"none", border:"none", color:"#555", cursor:"pointer", fontSize:"0.82rem" }}>← Volver</button>
        <div style={{ width:1, height:18, background:"#2a2a2a" }} />
        <span style={{ color:c.color, fontSize:"0.75rem", letterSpacing:"0.15em", textTransform:"uppercase" }}>{c.badge} {c.name}</span>
        <span style={{ marginLeft:"auto", color:"#444", fontSize:"0.78rem" }}>Biblioteca de Supuestos</span>
      </div>

      <div style={{ maxWidth:960, margin:"0 auto", padding:"2.5rem 1.5rem" }}>
        <h2 style={{ fontSize:"1.8rem", fontWeight:"300", fontFamily:"Georgia,serif", marginBottom:"0.3rem" }}>Biblioteca</h2>
        <p style={{ color:"#555", marginBottom:"2.5rem", fontSize:"0.85rem" }}>{supuestos.length} supuesto{supuestos.length!==1?"s":""} disponible{supuestos.length!==1?"s":""}</p>

        <div
          onDragOver={e => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={e => { e.preventDefault(); setDragOver(false); if (!busy) handleFile(e.dataTransfer.files[0]); }}
          onClick={() => !busy && fileRef.current.click()}
          style={{ border:`2px dashed ${status?.error?"#dc2626":status?.phase==="ok"?"#16a34a":dragOver?c.color:"rgba(255,255,255,0.1)"}`,
            borderRadius:8, padding:"2rem", textAlign:"center", marginBottom:"2rem",
            cursor:busy?"default":"pointer", transition:"all 0.3s",
            background:dragOver?`${c.color}07`:"rgba(255,255,255,0.015)" }}>
          <input ref={fileRef} type="file" accept=".pdf" style={{ display:"none" }}
            onChange={e => { handleFile(e.target.files[0]); e.target.value=""; }} />

          {busy ? (
            <div>
              <div style={{ fontSize:"1.6rem", marginBottom:"0.6rem" }}>🤖</div>
              <div style={{ color:c.color, fontSize:"0.88rem", marginBottom:"0.75rem" }}>{status.msg} <LoadingDots /></div>
              <div style={{ background:"#161618", borderRadius:99, height:3, overflow:"hidden", maxWidth:280, margin:"0 auto" }}>
                <div style={{ height:"100%", borderRadius:99, transition:"width 0.5s",
                  background:`linear-gradient(90deg,${c.color},${c.accent})`, width:`${status.progress}%` }} />
              </div>
            </div>
          ) : status?.phase==="ok" ? (
            <div style={{ color:"#4ade80", fontSize:"0.88rem" }}>{status.msg}</div>
          ) : status?.error ? (
            <div>
              <div style={{ color:"#f87171", fontSize:"0.88rem", marginBottom:"0.5rem" }}>⚠️ {status.error}</div>
              <button onClick={e => { e.stopPropagation(); setStatus(null); }}
                style={{ background:"none", border:"1px solid #444", color:"#888", borderRadius:4, padding:"0.3rem 0.8rem", cursor:"pointer", fontSize:"0.78rem" }}>
                Reintentar
              </button>
            </div>
          ) : (
            <div>
              <div style={{ fontSize:"2rem", marginBottom:"0.75rem" }}>📂</div>
              <div style={{ color:"#bbb", marginBottom:"0.3rem", fontSize:"0.95rem" }}>Arrastra un PDF o haz clic para subir</div>
              <div style={{ color:"#444", fontSize:"0.78rem" }}>La IA extraerá el enunciado y todas las preguntas tipo test</div>
            </div>
          )}
        </div>

        <div style={{ display:"flex", flexDirection:"column", gap:"0.75rem" }}>
          {supuestos.map((s, i) => (
            <div key={s.id||i} style={{ background:"rgba(255,255,255,0.025)", border:"1px solid rgba(255,255,255,0.07)",
              borderRadius:6, padding:"1.25rem 1.5rem", display:"flex", alignItems:"center", gap:"1.25rem" }}>
              <div style={{ width:42, height:42, borderRadius:6, background:`linear-gradient(135deg,${c.color}18,${c.accent}18)`,
                border:`1px solid ${c.color}25`, display:"flex", alignItems:"center", justifyContent:"center",
                fontSize:"1.2rem", flexShrink:0 }}>📋</div>
              <div style={{ flex:1, minWidth:0 }}>
                <div style={{ fontWeight:"600", fontSize:"0.9rem", marginBottom:"0.2rem", overflow:"hidden", textOverflow:"ellipsis", whiteSpace:"nowrap" }}>{s.titulo}</div>
                <div style={{ color:"#555", fontSize:"0.77rem" }}>{s.preguntas?.length||0} preguntas</div>
              </div>
              <div style={{ display:"flex", gap:"0.5rem", flexShrink:0 }}>
                <button onClick={() => onStartTest(s)} style={{
                  background:`linear-gradient(135deg,${c.color},${c.accent})`,
                  border:"none", color:"#09090f", fontWeight:"700",
                  padding:"0.55rem 1.3rem", borderRadius:4, cursor:"pointer",
                  fontSize:"0.82rem", whiteSpace:"nowrap" }}>
                  Iniciar Test
                </button>
                {s.id !== 0 && (
                  <button onClick={() => deleteSupuesto(s.id)} style={{
                    background:"rgba(220,38,38,0.08)", border:"1px solid rgba(220,38,38,0.2)",
                    color:"#f87171", borderRadius:4, padding:"0.55rem 0.7rem",
                    cursor:"pointer", fontSize:"0.8rem" }} title="Eliminar">
                    🗑
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ─── TEST ───────────────────────────────────────────── */
function TestView({ corp, supuesto: init, onBack }) {
  const [supuesto, setSupuesto] = useState(init);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [chat, setChat] = useState(null);
  const [chatInput, setChatInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [chatMsgs, setChatMsgs] = useState([]);
  const [enunciadoOpen, setEnunciadoOpen] = useState(true);
  const chatEndRef = useRef();
  const c = CORPS[corp];
  const total = supuesto.preguntas.length;
  const answered = Object.keys(answers).length;
  const score = submitted ? supuesto.preguntas.filter((p,i) => answers[i]===p.correcta).length : null;

  const handleSubmit = () => {
    if (answered < total && !confirm(`${total-answered} pregunta(s) sin responder. ¿Entregar igualmente?`)) return;
    setSubmitted(true);
    window.scrollTo({ top:0, behavior:"smooth" });
  };

  const openChat = (q, idx) => {
    setChat({ ...q, idx });
    setChatMsgs([{ role:"assistant", text:`📌 Pregunta ${idx+1}: ${q.texto}\n\n✅ Respuesta correcta: ${q.opciones[q.correcta]}\n\n📖 Explicación (con fundamento jurídico): ${q.explicacion}\n\n¿Tienes alguna duda o consideras que la respuesta marcada es incorrecta? Arguméntalo y lo analizaré aplicando el marco normativo.` }]);
    setTimeout(() => chatEndRef.current?.scrollIntoView({ behavior:"smooth" }), 100);
  };

  const sendChat = async () => {
    if (!chatInput.trim() || chatLoading) return;
    const msg = chatInput; setChatInput("");
    const msgs = [...chatMsgs, { role:"user", text:msg }];
    setChatMsgs(msgs); setChatLoading(true);
    setTimeout(() => chatEndRef.current?.scrollIntoView({ behavior:"smooth" }), 50);
    try {
      const r = await fetch("https://api.anthropic.com/v1/messages", {
        method:"POST", headers:{ "Content-Type":"application/json" },
        body: JSON.stringify({
          model:"claude-opus-4-5", max_tokens:1000,
          system:`Eres un experto jurídico en legislación policial española, especializado en oposiciones de Policía Canaria y Policía Local de Canarias.
OBLIGACIÓN: En CADA respuesta debes citar artículos y normas concretas del marco normativo. Nunca respondas sin fundamento legal.

${MARCO_NORMATIVO}

CONTEXTO DEL TEST:
Supuesto: ${supuesto.enunciado}
Pregunta (índice ${chat?.idx}): ${chat?.texto}
Opciones: ${chat?.opciones?.join(" | ")}
Respuesta correcta actual: ${chat?.opciones?.[chat?.correcta]} (índice ${chat?.correcta})

INSTRUCCIONES:
- Explica siempre el fundamento jurídico citando artículo y ley (ej: "art. 5.2.c LOFCS", "art. 492 LECrim").
- Si el usuario argumenta que la respuesta es incorrecta, analiza su razonamiento con rigor jurídico.
- Si le das la razón, incluye AL FINAL: JSON_CAMBIO:{"nueva_correcta":INDICE,"nueva_explicacion":"explicacion con cita legal"}
- Si no hay cambio no incluyas ese bloque.`,
          messages: msgs.map(m => ({ role:m.role==="user"?"user":"assistant", content:m.text }))
        })
      });
      const d = await r.json();
      let txt = d.content?.map(b => b.text||"").join("") || "";
      const cm = txt.match(/JSON_CAMBIO:(\{[^}]+\})/);
      if (cm) {
        try {
          const ch = JSON.parse(cm[1]);
          setSupuesto(prev => ({ ...prev, preguntas: prev.preguntas.map((p,i) =>
            i===chat.idx ? { ...p, correcta:ch.nueva_correcta, explicacion:ch.nueva_explicacion } : p) }));
          setChat(prev => ({ ...prev, correcta:ch.nueva_correcta, explicacion:ch.nueva_explicacion }));
          txt = txt.replace(/JSON_CAMBIO:\{[^}]+\}/,"").trim() + "\n\n✅ Respuesta actualizada en el test.";
        } catch {}
      }
      setChatMsgs(prev => [...prev, { role:"assistant", text:txt }]);
    } catch { setChatMsgs(prev => [...prev, { role:"assistant", text:"Error de conexión. Inténtalo." }]); }
    finally { setChatLoading(false); setTimeout(() => chatEndRef.current?.scrollIntoView({ behavior:"smooth" }), 100); }
  };

  const optStyle = (q, qIdx, optIdx) => {
    const sel = answers[qIdx];
    if (!submitted) return sel===optIdx
      ? { bg:`${c.color}1a`, border:c.color, color:"#f5f0e8", weight:"600" }
      : { bg:"rgba(255,255,255,0.025)", border:"rgba(255,255,255,0.08)", color:"#aaa", weight:"400" };
    if (optIdx===q.correcta) return { bg:"rgba(22,163,74,0.12)", border:"#16a34a", color:"#4ade80", weight:"600" };
    if (sel===optIdx)         return { bg:"rgba(220,38,38,0.1)",  border:"#dc2626", color:"#f87171", weight:"400" };
    return { bg:"rgba(255,255,255,0.015)", border:"rgba(255,255,255,0.05)", color:"#555", weight:"400" };
  };

  return (
    <div style={{ minHeight:"100vh", background:"#09090f", fontFamily:"system-ui,sans-serif", color:"#f0ece0" }}>

      {/* Top bar */}
      <div style={{ borderBottom:"1px solid rgba(255,255,255,0.06)", padding:"0.8rem 1.5rem",
        display:"flex", alignItems:"center", gap:"1rem", position:"sticky", top:0, zIndex:30,
        background:"rgba(9,9,15,0.95)", backdropFilter:"blur(14px)" }}>
        <button onClick={onBack} style={{ background:"none", border:"none", color:"#555", cursor:"pointer", fontSize:"0.82rem" }}>← Biblioteca</button>
        <div style={{ width:1, height:16, background:"#2a2a2a" }} />
        <span style={{ color:c.color, fontSize:"0.72rem", letterSpacing:"0.15em", textTransform:"uppercase" }}>{c.badge} {c.name}</span>
        <div style={{ marginLeft:"auto", display:"flex", alignItems:"center", gap:"1.25rem" }}>
          {!submitted ? (
            <>
              <span style={{ color:"#444", fontSize:"0.78rem" }}>{answered}/{total} respondidas</span>
              <button onClick={handleSubmit} style={{ background:`linear-gradient(135deg,${c.color},${c.accent})`,
                border:"none", color:"#09090f", fontWeight:"700", padding:"0.45rem 1.2rem",
                borderRadius:4, cursor:"pointer", fontSize:"0.8rem" }}>Entregar test</button>
            </>
          ) : (
            <span style={{ fontWeight:"700", fontSize:"0.88rem", color: score/total>=0.6?"#4ade80":"#f87171" }}>
              {score}/{total} correctas · {Math.round(score/total*100)}%
            </span>
          )}
        </div>
      </div>

      <div style={{ maxWidth:820, margin:"0 auto", padding:"1.5rem 1.25rem 5rem" }}>

        {/* Enunciado sticky */}
        <div style={{ position:"sticky", top:49, zIndex:20, marginBottom:"1.5rem" }}>
          <div style={{ background:"#0d0d16", border:`1px solid ${c.color}20`,
            borderLeft:`3px solid ${c.color}`, borderRadius:6, overflow:"hidden",
            boxShadow:"0 6px 30px rgba(0,0,0,0.6)" }}>
            <button onClick={() => setEnunciadoOpen(o=>!o)}
              style={{ width:"100%", background:"none", border:"none", cursor:"pointer",
                padding:"0.85rem 1.1rem", display:"flex", alignItems:"center", justifyContent:"space-between", color:"#f0ece0" }}>
              <div style={{ display:"flex", alignItems:"center", gap:"0.65rem" }}>
                <span style={{ fontSize:"0.58rem", color:c.color, letterSpacing:"0.25em", textTransform:"uppercase", flexShrink:0 }}>Supuesto</span>
                <span style={{ fontSize:"0.88rem", fontWeight:"600", fontFamily:"Georgia,serif", textAlign:"left" }}>{supuesto.titulo}</span>
              </div>
              <span style={{ color:"#444", fontSize:"0.72rem", flexShrink:0, marginLeft:"1rem",
                display:"inline-block", transition:"transform 0.2s", transform:enunciadoOpen?"rotate(180deg)":"rotate(0deg)" }}>▼</span>
            </button>
            {enunciadoOpen && (
              <div style={{ padding:"0 1.1rem 1.1rem", borderTop:"1px solid rgba(255,255,255,0.04)" }}>
                <p style={{ color:"#8a8280", fontSize:"0.84rem", lineHeight:1.78, margin:"0.85rem 0 0" }}>
                  {supuesto.enunciado}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Todas las preguntas */}
        <div style={{ display:"flex", flexDirection:"column", gap:"1rem" }}>
          {supuesto.preguntas.map((q, qIdx) => {
            const isCorrect  = submitted && answers[qIdx]===q.correcta;
            const isWrong    = submitted && answers[qIdx]!==undefined && answers[qIdx]!==q.correcta;
            const noAnswer   = submitted && answers[qIdx]===undefined;
            const borderCol  = isCorrect?"#16a34a45": isWrong?"#dc262645": noAnswer?"#55555545":"rgba(255,255,255,0.07)";

            return (
              <div key={q.id||qIdx} style={{ background:"rgba(255,255,255,0.02)", border:`1px solid ${borderCol}`,
                borderRadius:8, overflow:"hidden", transition:"border-color 0.3s" }}>

                {/* Header de pregunta */}
                <div style={{ padding:"0.95rem 1.1rem 0.7rem", display:"flex", gap:"0.75rem", alignItems:"flex-start" }}>
                  <div style={{ width:26, height:26, borderRadius:4, flexShrink:0, marginTop:2,
                    background: isCorrect?"rgba(22,163,74,0.15)": isWrong?"rgba(220,38,38,0.15)":`${c.color}12`,
                    border:`1px solid ${isCorrect?"#16a34a40": isWrong?"#dc262640": c.color+"28"}`,
                    display:"flex", alignItems:"center", justifyContent:"center", fontSize:"0.7rem", fontWeight:"700",
                    color: isCorrect?"#4ade80": isWrong?"#f87171": c.color }}>
                    {isCorrect?"✓": isWrong?"✗": qIdx+1}
                  </div>
                  <p style={{ flex:1, margin:0, fontSize:"0.87rem", lineHeight:1.65, color:"#ddd", fontWeight:"500" }}>
                    {q.texto}
                  </p>
                </div>

                {/* Opciones */}
                <div style={{ padding:"0 1.1rem 0.9rem", display:"flex", flexDirection:"column", gap:"0.45rem" }}>
                  {q.opciones.map((opt, optIdx) => {
                    const s = optStyle(q, qIdx, optIdx);
                    return (
                      <button key={optIdx}
                        onClick={() => !submitted && setAnswers(prev => ({...prev,[qIdx]:optIdx}))}
                        style={{ background:s.bg, border:`1.5px solid ${s.border}`, borderRadius:5,
                          padding:"0.55rem 0.85rem", textAlign:"left", cursor:submitted?"default":"pointer",
                          color:s.color, fontSize:"0.82rem", lineHeight:1.5, fontWeight:s.weight,
                          transition:"all 0.15s", display:"flex", alignItems:"center", gap:"0.55rem" }}>
                        <span style={{ width:19, height:19, borderRadius:"50%", flexShrink:0,
                          border:`1.5px solid ${s.border}`, display:"flex", alignItems:"center",
                          justifyContent:"center", fontSize:"0.62rem", color:s.color }}>
                          {submitted && optIdx===q.correcta?"✓": submitted && answers[qIdx]===optIdx && optIdx!==q.correcta?"✗": ["A","B","C","D"][optIdx]}
                        </span>
                        {opt}
                      </button>
                    );
                  })}
                </div>

                {/* Explicación tras entregar */}
                {submitted && (
                  <div style={{ margin:"0 1.1rem 0.9rem", padding:"0.75rem 0.9rem",
                    background: isCorrect?"rgba(22,163,74,0.05)": isWrong?"rgba(220,38,38,0.05)":"rgba(255,255,255,0.02)",
                    border:`1px solid ${isCorrect?"#16a34a22": isWrong?"#dc262622":"#ffffff0d"}`,
                    borderRadius:5, display:"flex", gap:"0.85rem", alignItems:"flex-start" }}>
                    <div style={{ flex:1 }}>
                      <div style={{ fontSize:"0.6rem", textTransform:"uppercase", letterSpacing:"0.15em", color:"#3a3a3a", marginBottom:"0.28rem" }}>Explicación</div>
                      <p style={{ margin:0, fontSize:"0.8rem", color:"#777", lineHeight:1.65 }}>{q.explicacion}</p>
                    </div>
                    <button onClick={() => openChat(q, qIdx)} style={{ flexShrink:0, background:`${c.color}0d`,
                      border:`1px solid ${c.color}25`, color:c.color, borderRadius:4,
                      padding:"0.32rem 0.65rem", cursor:"pointer", fontSize:"0.7rem", whiteSpace:"nowrap" }}>
                      🤖 Consultar
                    </button>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Botón entregar al final */}
        {!submitted && (
          <div style={{ marginTop:"2rem", textAlign:"center" }}>
            <button onClick={handleSubmit} style={{ background:`linear-gradient(135deg,${c.color},${c.accent})`,
              border:"none", color:"#09090f", fontWeight:"700", padding:"0.8rem 3rem",
              borderRadius:6, cursor:"pointer", fontSize:"0.9rem", letterSpacing:"0.04em" }}>
              Entregar test · {answered}/{total} respondidas
            </button>
          </div>
        )}
      </div>

      {/* Chat drawer */}
      {chat && (
        <div style={{ position:"fixed", inset:0, background:"rgba(0,0,0,0.75)", backdropFilter:"blur(4px)",
          display:"flex", alignItems:"flex-end", justifyContent:"center", zIndex:50 }}>
          <div style={{ background:"#0d0d16", border:`1px solid ${c.color}18`, borderRadius:"10px 10px 0 0",
            width:"100%", maxWidth:700, height:"60vh", display:"flex", flexDirection:"column",
            boxShadow:"0 -20px 60px rgba(0,0,0,0.7)" }}>
            <div style={{ padding:"0.75rem 1.25rem", borderBottom:"1px solid rgba(255,255,255,0.06)",
              display:"flex", alignItems:"center", justifyContent:"space-between" }}>
              <div style={{ display:"flex", alignItems:"center", gap:"0.6rem" }}>
                <div style={{ width:26, height:26, borderRadius:"50%", background:`${c.color}15`,
                  border:`1px solid ${c.color}30`, display:"flex", alignItems:"center", justifyContent:"center", fontSize:"0.8rem" }}>🤖</div>
                <div>
                  <div style={{ fontSize:"0.78rem", fontWeight:"600" }}>Asistente · Pregunta {chat.idx+1}</div>
                  <div style={{ fontSize:"0.62rem", color:"#444" }}>Puede corregir respuestas incorrectas</div>
                </div>
              </div>
              <button onClick={() => setChat(null)} style={{ background:"none", border:"none", color:"#444", cursor:"pointer", fontSize:"1.3rem", lineHeight:1 }}>×</button>
            </div>
            <div style={{ flex:1, overflowY:"auto", padding:"0.85rem 1.25rem", display:"flex", flexDirection:"column", gap:"0.65rem" }}>
              {chatMsgs.map((m,i) => (
                <div key={i} style={{ display:"flex", justifyContent:m.role==="user"?"flex-end":"flex-start" }}>
                  <div style={{ maxWidth:"88%", padding:"0.55rem 0.8rem", borderRadius:7,
                    background:m.role==="user"?`${c.color}12`:"rgba(255,255,255,0.03)",
                    border:`1px solid ${m.role==="user"?c.color+"28":"rgba(255,255,255,0.05)"}`,
                    fontSize:"0.8rem", lineHeight:1.65, color:"#ccc", whiteSpace:"pre-wrap" }}>
                    {m.text}
                  </div>
                </div>
              ))}
              {chatLoading && <div style={{ color:"#444", fontSize:"0.78rem" }}><LoadingDots /></div>}
              <div ref={chatEndRef} />
            </div>
            <div style={{ padding:"0.75rem 1.25rem", borderTop:"1px solid rgba(255,255,255,0.06)", display:"flex", gap:"0.5rem" }}>
              <input value={chatInput} onChange={e=>setChatInput(e.target.value)}
                onKeyDown={e=>e.key==="Enter"&&!e.shiftKey&&sendChat()}
                placeholder="Pregunta o argumenta si la respuesta es incorrecta…"
                style={{ flex:1, background:"rgba(255,255,255,0.04)", border:"1px solid rgba(255,255,255,0.08)",
                  borderRadius:5, padding:"0.58rem 0.82rem", color:"#f0ece0", fontSize:"0.8rem", outline:"none" }} />
              <button onClick={sendChat} disabled={chatLoading||!chatInput.trim()}
                style={{ background:chatLoading||!chatInput.trim()?"#181820":`linear-gradient(135deg,${c.color},${c.accent})`,
                  border:"none", color:"#09090f", fontWeight:"700", padding:"0.58rem 1rem",
                  borderRadius:5, cursor:"pointer", fontSize:"0.85rem" }}>→</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* ─── ROOT ───────────────────────────────────────────── */
export default function App() {
  const [screen, setScreen] = useState("home");
  const [corp, setCorp] = useState(null);
  const [supuesto, setSupuesto] = useState(null);
  if (screen==="home")    return <CorpSelector onSelect={id => { setCorp(id); setScreen("library"); }} />;
  if (screen==="library") return <Library corp={corp} onBack={() => setScreen("home")} onStartTest={s => { setSupuesto(s); setScreen("test"); }} />;
  if (screen==="test")    return <TestView corp={corp} supuesto={supuesto} onBack={() => setScreen("library")} />;
}
