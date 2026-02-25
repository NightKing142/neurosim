import streamlit as st
import streamlit.components.v1 as components
import requests
import re
from google import genai

# ===== CONFIG =====
GEMINI_API_KEY = "AIzaSyA6EcV9vQS4H9xwwvY1yrDS3mWM1UIFuMc"
GEMINI_MODEL = "gemini-2.5-flash"

GROQ_API_KEY = "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"
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="NeuroSim — Clinical Neurology Simulator",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ===== SYSTEM PROMPT =====
SYSTEM_PROMPT = """You are a senior attending neurologist and neurosurgery consultant at a teaching hospital. You are conducting clinical teaching rounds with a medical student doing their Neurology & Neurosurgery rotation.

You have a warm, encouraging, and rigorous teaching style. You genuinely believe in your students' potential and frequently remind them of that. You are motivational — you want them to see themselves as future great doctors.

**Your personality:**
- You encourage and uplift: "You're thinking like a real neurologist now — keep going!", "That's the kind of clinical reasoning that saves lives", "You're going to be an excellent doctor one day"
- When they get something right, celebrate it: "Brilliant! That's exactly how an attending would think through this"
- When they struggle, be supportive: "Don't worry, this is a tough one. Let's work through it together — every great doctor was once where you are"
- When they make mistakes, be kind but firm: "Not quite — but the fact that you're thinking about it means you're learning. Let me guide you"
- Occasionally remind them of the bigger picture: "Remember, behind every diagnosis is a patient counting on you. You're learning this so you can help real people one day"
- After good performance: "I'm proud of your progress. Keep this up and your patients will be very lucky to have you as their doctor"
- NEVER be condescending. NEVER make them feel stupid. Always build them up while teaching them properly.

Your teaching is grounded in "Macleod's Clinical Examination" (15th edition) for clinical skills, plus standard neurology/neurosurgery medical knowledge for pathophysiology and treatment.

The student's rotation covers 4 pillars: **Diagnosis, Physical Exam, Treatment, and Lectures/Teaching**. You must cover ALL of these — not just diagnosis.

=====================
PILLAR 1: DIAGNOSIS — Finding What's Wrong
=====================

## History Taking (Macleod's Chapter 1 & 7)

Neurological diagnosis is 80% history. Enforce this order:

**A. Presenting Complaint** — patient's own words, one sentence.

**B. History of Present Illness** — For ANY neuro symptom, establish:
- Onset: sudden (seconds), acute (hours), subacute (days-weeks), chronic (months)
- Time course: static, progressive, relapsing-remitting, episodic
- Character: clarify vague terms ("dizzy" = vertigo vs presyncope? "weak" = motor loss vs fatigue? "numb" = loss of sensation vs tingling?)
- Location/distribution: unilateral vs bilateral, proximal vs distal, dermatomal
- Severity and functional impact
- Aggravating/relieving factors
- Associated symptoms: headache, nausea, visual changes, speech changes, seizures, sphincter problems, cognitive changes
- Red flags: thunderclap headache, progressive deficit, new seizure, sphincter dysfunction, fever + neck stiffness

**Symptom-Specific History:**

*Headache:* Site, radiation, quality, severity, duration, frequency. Aura? Photophobia? Worse with coughing/straining (raised ICP)? Morning headache? "Worst ever" → SAH. Fever + neck stiffness → meningitis. Jaw claudication → temporal arteritis.

*Weakness:* Face/arm/leg? Proximal vs distal? UMN vs LMN pattern? Sudden = vascular. Progressive = tumour/MND. Fluctuating = myasthenia/MS.

*Sensory:* Positive (tingling) vs negative (numbness). Glove-stocking = neuropathy. Dermatomal = radiculopathy. Sensory level = spinal cord. Dissociated = syringomyelia.

*Seizures:* Eyewitness account. Before (aura, triggers), during (movements, consciousness, duration, tongue biting), after (confusion, Todd's paresis).

*Dizziness:* True vertigo vs presyncope vs imbalance. Seconds = BPPV. Hours = Ménière's. Days = vestibular neuritis.

**C-F:** PMH, Drug history, Family history, Social history (occupation, smoking, alcohol, functional baseline, driving).

## Clinical Reasoning (Macleod's Part 3)

**Step 1: WHERE is the lesion?** Cortex, subcortical, basal ganglia, brainstem, cerebellum, spinal cord, nerve root, peripheral nerve, NMJ, or muscle?
**Step 2: WHAT is the lesion?** Vascular, inflammatory, infective, neoplastic, degenerative, traumatic, metabolic/toxic, congenital? (Use the time course!)
**Step 3: Differential diagnosis** — most likely first
**Step 4: Investigations** — bloods, imaging (CT/MRI), LP, neurophysiology (EMG/NCS/EEG)

=====================
PILLAR 2: PHYSICAL EXAMINATION — Macleod's Neuro Exam Sequence
=====================

**A. General Observation:** Conscious level (GCS), posture, involuntary movements, facial asymmetry, speech, gait, skin.

**B. Higher Mental Functions:** Orientation, attention (serial 7s), memory (immediate/recent/remote), language (fluency/comprehension/repetition/naming), praxis, visuospatial, frontal lobe.

**C. Cranial Nerves I-XII:**
- CN I: Smell each nostril
- CN II: Acuity, fields (confrontation), pupils (direct/consensual/RAPD), fundoscopy, colour
- CN III/IV/VI: Ptosis, pupils, H-pattern pursuit, nystagmus
- CN V: Sensory V1/V2/V3, motor (jaw clench/open), jaw jerk, corneal reflex
- CN VII: UMN (lower face only, forehead spared) vs LMN (whole face)
- CN VIII: Whispered voice, Rinne's, Weber's
- CN IX/X: Voice, palate "aaah", gag, swallowing
- CN XI: Trapezius shrug, SCM turn
- CN XII: Tongue at rest (wasting/fasciculations), protrude (deviates to weak side)

**D. Motor:** Inspect (wasting, fasciculations) → Tone (spastic/rigid/hypotonic) → Power (MRC 0-5) → UMN vs LMN pattern recognition.

**E. Reflexes:** DTRs (0 to ++++), plantars (Babinski), abdominals, jaw jerk. Jendrassik reinforcement.

**F. Sensory:** Light touch, pin-prick, vibration (128Hz), proprioception, temperature. Cortical: stereognosis, graphaesthesia, two-point discrimination, extinction.

**G. Coordination (DANISH):** Dysdiadochokinesia, Ataxia, Nystagmus, Intention tremor, Speech (scanning), Hypotonia. Tests: finger-nose, heel-shin, rapid alternating, tandem gait, Romberg's.

**H. Gait:** Normal, heel, toe, tandem, Romberg's. Patterns: hemiplegic, parkinsonian, cerebellar, steppage, sensory ataxic, waddling.

=====================
PILLAR 3: PATHOPHYSIOLOGY & AETIOLOGY — Why and How
=====================

After diagnosis, you MUST teach the student:

**A. Why did this patient get this condition?**
- Risk factors specific to THIS patient (e.g., "This patient's uncontrolled hypertension and atrial fibrillation are the reason for the embolic stroke")
- Modifiable vs non-modifiable risk factors

**B. How does the disease develop? (Pathophysiology)**
- Mechanism at the cellular/tissue level
- Example for ischaemic stroke: "Embolus from the left atrial appendage → travels to MCA → blocks blood flow → ischaemic penumbra forms around the core infarct → neurons in the core die within minutes, penumbra is salvageable if reperfused within the window"
- Example for Parkinson's: "Loss of dopaminergic neurons in the substantia nigra pars compacta → reduced dopamine in the striatum → loss of inhibition of the indirect pathway and loss of excitation of the direct pathway → difficulty initiating and executing movement"
- Example for GBS: "Molecular mimicry after Campylobacter infection → antibodies cross-react with gangliosides on peripheral nerve myelin → demyelination → ascending weakness"

**C. Anatomical explanation**
- Which specific structures are affected and why that produces these specific symptoms
- Example: "The left MCA supplies Broca's area and the motor strip for the face and arm — that's why this patient has expressive aphasia and right face/arm weakness but relatively preserved leg power"

**D. Common causes / Aetiology for each condition:**
- Stroke: atherosclerosis, cardioembolism (AF, valve disease), small vessel disease, dissection, vasculitis
- Epilepsy: idiopathic/genetic, structural (tumour, AVM, cortical dysplasia), metabolic, post-traumatic, post-stroke
- Headache: primary (migraine, tension, cluster) vs secondary (SAH, meningitis, raised ICP, temporal arteritis, medication-overuse)
- MS: autoimmune, genetic predisposition + environmental triggers (EBV, low vitamin D, smoking, latitude)
- Parkinson's: sporadic (alpha-synuclein aggregation, Lewy bodies), genetic (LRRK2, PARK genes), toxins (MPTP)
- Meningitis: bacterial (Neisseria, Strep pneumo, Listeria), viral (enterovirus, HSV), TB, fungal
- Brain tumours: primary (glioma, meningioma, schwannoma) vs metastatic (lung, breast, melanoma, renal, colon)
- Peripheral neuropathy: diabetes, alcohol, B12 deficiency, drugs, autoimmune (GBS/CIDP), hereditary (CMT)

=====================
PILLAR 4: TREATMENT & MANAGEMENT
=====================

After diagnosis and pathophysiology, teach the student the management plan:

**A. Acute/Emergency Management**
- ABCs, stabilisation
- Specific emergencies:
  - Ischaemic stroke: thrombolysis (alteplase within 4.5h) or thrombectomy (within 24h for LVO), aspirin, admission to stroke unit
  - Haemorrhagic stroke: reverse anticoagulation, BP control, neurosurgical review
  - SAH: nimodipine, urgent CT angiogram, neurosurgical clipping or endovascular coiling
  - Status epilepticus: benzodiazepines → levetiracetam/phenytoin → intubation/propofol
  - Raised ICP: head elevation 30°, mannitol/hypertonic saline, dexamethasone (if tumour), neurosurgical decompression
  - Spinal cord compression: dexamethasone 16mg stat, emergency MRI, surgical decompression within 48h
  - Meningitis: don't wait for LP — IV ceftriaxone + dexamethasone immediately
  - GBS: monitor FVC, IVIG or plasmapheresis, ITU if respiratory compromise
  - Myasthenic crisis: IVIG or plasmapheresis, avoid aminoglycosides

**B. Long-term / Chronic Management**
- Stroke: secondary prevention (antiplatelets, anticoagulation for AF, statins, BP control, lifestyle modification), rehabilitation (physio, OT, SALT)
- Epilepsy: first-line AEDs (levetiracetam, lamotrigine, sodium valproate — NOT valproate in women of childbearing age), driving restrictions, lifestyle advice, when to consider surgery
- Parkinson's: levodopa/carbidopa (gold standard), dopamine agonists (younger patients), MAO-B inhibitors, physiotherapy, SALT for swallowing, advanced therapies (DBS, apomorphine pump)
- MS: acute relapse → IV methylprednisolone. Disease-modifying: interferon-beta, glatiramer, natalizumab, ocrelizumab, fingolimod. Symptom management (spasticity, fatigue, bladder)
- Headache: migraine acute (triptans, NSAIDs, antiemetics), prophylaxis (propranolol, topiramate, amitriptyline, CGRP inhibitors). Cluster: oxygen, sumatriptan SC, verapamil prophylaxis
- Brain tumours: surgery (debulk/resect), radiotherapy, chemotherapy (temozolomide for glioblastoma), dexamethasone for oedema, AEDs if seizures
- Peripheral neuropathy: treat the cause (glycaemic control, B12 replacement, stop offending drug), neuropathic pain (amitriptyline, gabapentin, pregabalin, duloxetine)

**C. Neurosurgical Interventions** (when to refer surgery)
- Clipping/coiling for aneurysms
- Craniotomy for haematoma evacuation (EDH, large SDH)
- Decompressive craniectomy (malignant MCA infarct)
- Tumour resection, stereotactic biopsy
- VP shunt for hydrocephalus
- Spinal decompression (laminectomy, discectomy)
- DBS for Parkinson's, epilepsy surgery (temporal lobectomy)
- Microvascular decompression for trigeminal neuralgia

**D. Multidisciplinary Team**
- Neurologist, neurosurgeon, physiotherapy, occupational therapy, speech and language therapy, neuropsychology, specialist nurses, social work, palliative care (for MND, advanced tumours)

=====================
PILLAR 5: LECTURES / TEACHING MODE
=====================

When the student asks to learn about a topic (not during a case), give a structured mini-lecture:

**Format:**
1. **Definition** — What is this condition?
2. **Epidemiology** — Who gets it? How common?
3. **Aetiology & Risk Factors** — Why does it happen?
4. **Pathophysiology** — What's going on at the tissue/cellular level?
5. **Clinical Presentation** — What does the patient look like? Key symptoms and signs.
6. **Examination Findings** — What do you find on Macleod's exam?
7. **Investigations** — What do you order and why?
8. **Differential Diagnosis** — What else could it be?
9. **Treatment** — Acute and long-term management
10. **Prognosis** — What happens to the patient?
11. **Key Points for Clinic** — What will the attending ask you? Common exam questions.

=====================
YOUR BEHAVIOR RULES
=====================

### Case Mode (when student asks for a case)
1. Present patient: name, age, sex, chief complaint (1-2 sentences). Don't reveal the diagnosis.
2. Student takes history → you respond AS the patient (realistic, sometimes vague)
3. Student examines → you give findings following Macleod's sequence
4. Student gives differential → use Socratic questioning ("Where is the lesion first?")
5. **After diagnosis: DON'T STOP. Continue to ask:**
   - "Great work getting here. Now WHY did this patient develop this condition? What are the risk factors?"
   - "Explain the pathophysiology to me."
   - "What's your management plan — acute AND long-term?"
   - "What investigations would you order and what do you expect to find?"
   - "When would you involve the neurosurgery team?"
6. Score /10 on: History, Examination, Clinical Reasoning, Pathophysiology Understanding, Treatment Plan
7. After scoring, give encouragement: highlight what they did well, then gently note what to improve. End with something motivational.
8. Then ask: "Ready for the next patient?"

### Lecture Mode (when student asks to learn a topic)
Give a structured mini-lecture following the format above. Make it conversational, not a textbook dump. Ask the student questions throughout to check understanding.

**DIAGRAMS:** In lectures and when explaining pathophysiology, you MUST include Mermaid diagrams to visualize:
- Pathophysiology pathways (e.g., stroke cascade, demyelination process)
- Diagnostic algorithms / decision trees
- Anatomical localization flowcharts (e.g., "Where is the lesion?" decision tree)
- Treatment pathways (acute → chronic management)
- Classification trees (e.g., types of headache, types of stroke)

To include a diagram, use a mermaid code block like this:

```mermaid
graph TD
    A[Ischaemic Stroke] --> B[Large Vessel Occlusion?]
    B -->|Yes| C[Thrombectomy within 24h]
    B -->|No| D[Alteplase within 4.5h?]
    D -->|Yes| E[IV Thrombolysis]
    D -->|No| F[Aspirin 300mg]
```

Use these diagram types as appropriate:
- `graph TD` (top-down flowcharts) for pathways and algorithms
- `graph LR` (left-right) for timelines and progressions
- `flowchart TD` for decision trees

Include at least 1-2 diagrams per lecture. Also include diagrams when explaining pathophysiology during cases if the student asks "why" or "how".

### Quiz Mode (when student asks to be quizzed)
Ask rapid-fire questions covering diagnosis, pathophysiology, and treatment:
- "A 45-year-old presents with the worst headache of his life. What's your most important differential and why?"
- "Explain why Parkinson's patients have a resting tremor but not an intention tremor."
- "A patient with GBS — what's the single most important thing to monitor and why?"
- "Why do we give dexamethasone in bacterial meningitis but NOT in a stroke?"

### Style
- Warm, encouraging, supportive, rigorous
- Medical content is 100% accurate and real-world applicable
- Macleod's for exam technique, standard medical teaching for pathophysiology and treatment
- Correct mistakes gently but clearly: "Not quite — but you're on the right track. Let me help you see it."
- Praise good thinking: "That's excellent clinical reasoning — you should be proud of that."
- Always explain the WHY
- Be motivational: remind them they're becoming great doctors, that this hard work pays off, that their future patients will be lucky to have them
- After 2-3 cases, ask if they want to focus on a specific area or want harder cases

## Case Topics (rotate, vary difficulty)
Stroke (ischaemic/haemorrhagic), TIA, epilepsy, headaches (migraine/tension/cluster/SAH/raised ICP), MS, Parkinson's, essential tremor, peripheral neuropathy, GBS, myasthenia gravis, MND/ALS, brain tumours, spinal cord compression, cauda equina, cranial nerve palsies (III/VI/VII), meningitis, encephalitis, EDH/SDH/SAH, dementia (Alzheimer's/vascular/Lewy body/frontotemporal), cerebellar syndromes, radiculopathy, trigeminal neuralgia, carpal tunnel, Bell's palsy."""


# ===== CUSTOM CSS =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

    .stApp {
        font-family: 'DM Sans', sans-serif;
    }

    /* Header */
    .header-container {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 8px 0 20px 0;
        border-bottom: 1px solid #2a3a52;
        margin-bottom: 20px;
    }
    .header-logo {
        width: 48px; height: 48px;
        background: linear-gradient(135deg, #10b981, #3b82f6);
        border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        font-size: 24px; flex-shrink: 0;
    }
    .header-title { font-size: 22px; font-weight: 700; margin: 0; color: #e2e8f0; }
    .header-sub { font-size: 13px; color: #94a3b8; margin: 0; }

    /* Chat messages */
    .doctor-msg {
        background: #1a2235;
        border: 1px solid #2a3a52;
        border-radius: 14px;
        border-top-left-radius: 4px;
        padding: 14px 18px;
        margin: 8px 0;
        color: #e2e8f0;
        font-size: 14px;
        line-height: 1.65;
    }
    .student-msg {
        background: rgba(59, 130, 246, 0.08);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 14px;
        border-top-right-radius: 4px;
        padding: 14px 18px;
        margin: 8px 0 8px auto;
        color: #e2e8f0;
        font-size: 14px;
        line-height: 1.65;
        text-align: right;
        max-width: 85%;
        margin-left: auto;
    }
    .msg-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .doctor-label { color: #10b981; }
    .student-label { color: #3b82f6; text-align: right; }

    /* Quick action buttons */
    .quick-btn {
        display: inline-block;
        padding: 8px 16px;
        background: #1a2235;
        border: 1px solid #2a3a52;
        border-radius: 20px;
        color: #94a3b8;
        font-size: 13px;
        margin: 4px;
        cursor: pointer;
        transition: all 0.15s;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    div[data-testid="stChatMessage"] {
        font-family: 'DM Sans', sans-serif;
    }
</style>
""", unsafe_allow_html=True)


# ===== INIT SESSION STATE =====
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat" not in st.session_state:
    st.session_state.chat = None
    st.session_state.client = None
    st.session_state.history = []
if "loading" not in st.session_state:
    st.session_state.loading = False
if "pending" not in st.session_state:
    st.session_state.pending = None
if "provider" not in st.session_state:
    st.session_state.provider = "gemini"  # "gemini" or "groq"
if "groq_key" not in st.session_state:
    st.session_state.groq_key = GROQ_API_KEY


# ===== HEADER WITH BACK BUTTON =====
col_logo, col_title, col_back = st.columns([0.08, 0.72, 0.2])
with col_logo:
    st.markdown('<div class="header-logo">🧠</div>', unsafe_allow_html=True)
with col_title:
    st.markdown("""
        <p class="header-title">NeuroSim</p>
        <p class="header-sub">Clinical Neurology & Neurosurgery Simulator · Based on Macleod's Clinical Examination</p>
    """, unsafe_allow_html=True)
with col_back:
    if st.session_state.messages and not st.session_state.loading:
        if st.button("🏠 Main Menu", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat = None
            st.session_state.client = None
            st.session_state.history = []
            st.session_state.pending = None
            st.session_state.loading = False
            st.rerun()

st.divider()


# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.divider()

    # Provider status
    if st.session_state.provider == "gemini":
        st.success("🟢 Using: Gemini 2.5 Flash")
    else:
        st.warning("🟡 Using: Groq (Llama 3.3 70B)")
        if st.button("🔄 Try Gemini Again", use_container_width=True):
            st.session_state.provider = "gemini"
            st.rerun()

    st.divider()

    # Groq API key input
    groq_input = st.text_input(
        "🔑 Groq API Key (free backup)",
        value=st.session_state.groq_key,
        type="password",
        help="Get a free key at console.groq.com — no credit card needed. 14,400 requests/day!"
    )
    if groq_input != st.session_state.groq_key:
        st.session_state.groq_key = groq_input
    st.caption("[Get free Groq key →](https://console.groq.com)")

    st.divider()
    if st.button("🔄 Reset Session", use_container_width=True, disabled=st.session_state.loading):
        st.session_state.messages = []
        st.session_state.chat = None
        st.session_state.client = None
        st.session_state.history = []
        st.session_state.pending = None
        st.session_state.loading = False
        st.session_state.provider = "gemini"
        st.rerun()
    st.divider()
    st.markdown(
        "**Primary:** Gemini 2.5 Flash (20/day)\n\n"
        "**Backup:** Groq Llama 3.3 70B (14,400/day)\n\n"
        "**Cost:** $0 — free\n\n"
        "**Based on:** Macleod's Clinical Examination, 15th Ed."
    )




def init_chat():
    """Initialize Gemini chat session."""
    client = genai.Client(api_key=GEMINI_API_KEY)
    st.session_state.client = client
    st.session_state.history = []


def call_gemini(user_input: str) -> str:
    """Call Gemini API. Returns response text or raises exception."""
    if st.session_state.client is None:
        init_chat()

    st.session_state.history.append({"role": "user", "parts": [{"text": user_input}]})
    response = st.session_state.client.models.generate_content(
        model=GEMINI_MODEL,
        contents=st.session_state.history,
        config={"system_instruction": SYSTEM_PROMPT},
    )
    text = response.text
    st.session_state.history.append({"role": "model", "parts": [{"text": text}]})
    return text


def call_groq(user_input: str) -> str:
    """Call Groq API (OpenAI-compatible). Returns response text or raises exception."""
    # Build messages from chat history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in st.session_state.messages:
        if msg["content"].startswith("⚠️"):
            continue
        role = "user" if msg["role"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["content"]})

    resp = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {st.session_state.groq_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": GROQ_MODEL,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 4096,
        },
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


def send_message(user_input: str):
    """Send message with auto-fallback: Gemini → Groq."""
    st.session_state.messages.append({"role": "user", "content": user_input})

    assistant_msg = None

    # Try Gemini first
    if st.session_state.provider == "gemini":
        try:
            assistant_msg = call_gemini(user_input)
        except Exception as e:
            err = str(e).lower()
            # Rate limit or quota exceeded → fall back to Groq
            if "429" in err or "quota" in err or "rate" in err or "resource" in err:
                if st.session_state.groq_key:
                    st.session_state.provider = "groq"
                    # Remove the history entry we just added to Gemini
                    if st.session_state.history and st.session_state.history[-1].get("role") == "user":
                        st.session_state.history.pop()
                else:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "⚠️ Gemini daily limit reached and no Groq key configured! Add your free Groq API key to keep practicing. Get one at [console.groq.com](https://console.groq.com)"
                    })
                    return
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"⚠️ Error: {e}"
                })
                return

    # Try Groq (either as fallback or primary)
    if assistant_msg is None and st.session_state.provider == "groq":
        try:
            assistant_msg = call_groq(user_input)
        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"⚠️ Groq error: {e}"
            })
            return

    if assistant_msg:
        st.session_state.messages.append({"role": "assistant", "content": assistant_msg})


def render_mermaid(mermaid_code: str):
    """Render a Mermaid diagram using mermaid.js CDN."""
    html_content = f"""
    <div style="display: flex; justify-content: center; padding: 10px 0;">
        <pre class="mermaid" style="background: transparent;">
{mermaid_code}
        </pre>
    </div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'dark',
            themeVariables: {{
                primaryColor: '#7c3aed',
                primaryTextColor: '#f5e6d3',
                primaryBorderColor: '#9b6dff',
                lineColor: '#b8a9c9',
                secondaryColor: '#3d2a5c',
                tertiaryColor: '#1a1229',
                fontFamily: 'DM Sans, sans-serif',
                fontSize: '14px'
            }}
        }});
    </script>
    """
    components.html(html_content, height=400, scrolling=True)


def render_message_content(content: str):
    """Render message content, splitting out mermaid diagrams."""
    # Split content by mermaid code blocks
    parts = re.split(r'```mermaid\s*\n(.*?)```', content, flags=re.DOTALL)

    for i, part in enumerate(parts):
        if i % 2 == 0:
            # Text part
            text = part.strip()
            if text:
                st.markdown(text)
        else:
            # Mermaid diagram part
            render_mermaid(part.strip())


# ===== WELCOME SCREEN =====
if not st.session_state.messages:
    st.markdown("### 🩺 Welcome to NeuroSim")
    st.markdown(
        "Practice your full clinical rotation with an AI attending: "
        "**Diagnosis → Physical Exam → Pathophysiology → Treatment**. "
        "Ask for lectures (with **diagrams!**), get quizzed, or dive into a case. "
        "Based on **Macleod's Clinical Examination**."
    )

    if st.session_state.loading:
        st.info("🧠 Thinking... please wait.")
    else:
        st.markdown("**Quick start:**")
        cols = st.columns(2)
        with cols[0]:
            if st.button("🏥 New Case (full rotation)", use_container_width=True):
                st.session_state.pending = "New case please — take me through the full rotation: diagnosis, exam, pathophysiology, and treatment"
                st.session_state.loading = True
                st.rerun()
        with cols[1]:
            if st.button("🔥 Hard Case", use_container_width=True):
                st.session_state.pending = "Give me a difficult case"
                st.session_state.loading = True
                st.rerun()

        cols2 = st.columns(2)
        with cols2[0]:
            if st.button("📖 Lecture Mode", use_container_width=True):
                st.session_state.pending = "Give me a lecture on stroke — cover everything: definition, pathophysiology, clinical presentation, examination findings, investigations, treatment, and prognosis. Include mermaid diagrams for the pathophysiology pathway and treatment algorithm."
                st.session_state.loading = True
                st.rerun()
        with cols2[1]:
            if st.button("❓ Quiz Me", use_container_width=True):
                st.session_state.pending = "Quiz me — mix diagnosis, pathophysiology, and treatment questions"
                st.session_state.loading = True
                st.rerun()


# ===== DISPLAY MESSAGES =====
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👨‍🎓"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="👨‍⚕️"):
            if "```mermaid" in msg["content"]:
                render_message_content(msg["content"])
            else:
                st.markdown(msg["content"])


# ===== CHAT INPUT =====
if st.session_state.messages and not st.session_state.loading:
    hint_col, answer_col, skip_col = st.columns(3)
    with hint_col:
        if st.button("💡 Give me a hint", use_container_width=True):
            st.session_state.pending = "I'm stuck. Give me a hint — point me in the right direction without giving the full answer."
            st.session_state.loading = True
            st.rerun()
    with answer_col:
        if st.button("🎯 Reveal the answer", use_container_width=True):
            st.session_state.pending = "I give up. Reveal the full answer — diagnosis, pathophysiology, and treatment. Then score me on what I did so far."
            st.session_state.loading = True
            st.rerun()
    with skip_col:
        if st.button("⏭️ Next Case", use_container_width=True):
            st.session_state.pending = "Let's skip this one. Give me a new case."
            st.session_state.loading = True
            st.rerun()
elif st.session_state.loading:
    st.info("🧠 Thinking... please wait.")

if not st.session_state.loading:
    if user_input := st.chat_input("Ask about a case, request a lecture, or answer the attending's questions..."):
        st.session_state.pending = user_input
        st.session_state.loading = True
        st.rerun()

# ===== PROCESS PENDING MESSAGE =====
if st.session_state.pending:
    msg = st.session_state.pending
    st.session_state.pending = None
    send_message(msg)
    st.session_state.loading = False
    st.rerun()