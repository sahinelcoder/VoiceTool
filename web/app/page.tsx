export default function Home() {
  return (
    <div className="min-h-screen font-sans">
      {/* Hero */}
      <section className="relative flex flex-col items-center justify-center min-h-screen px-6 overflow-hidden">
        {/* Background glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-accent/5 blur-[120px] pointer-events-none" />

        <div className="relative z-10 flex flex-col items-center text-center max-w-3xl">
          {/* Mic icon with pulse */}
          <div className="relative mb-10">
            <div className="absolute inset-0 rounded-full bg-accent/20 pulse-ring" />
            <div className="relative w-20 h-20 flex items-center justify-center rounded-full bg-card border border-card-border">
              <svg
                width="32"
                height="32"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="text-accent"
              >
                <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
                <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                <line x1="12" x2="12" y1="19" y2="22" />
              </svg>
            </div>
          </div>

          <h1 className="text-5xl sm:text-7xl font-bold tracking-tight animate-fade-in-up">
            Sprich.{" "}
            <span className="text-accent">Fertig.</span>
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-muted max-w-xl animate-fade-in-up-delay">
            Voice-Dictation für macOS. Hotkey halten, sprechen, loslassen
            — bereinigter Text erscheint im aktiven Textfeld.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 mt-10 animate-fade-in-up-delay-2">
            <a
              href="#features"
              className="inline-flex items-center justify-center h-12 px-8 rounded-full bg-accent text-white font-medium transition-colors hover:bg-accent-hover"
            >
              Mehr erfahren
            </a>
            <a
              href="https://github.com/sahinelcoder/VoiceTool"
              className="inline-flex items-center justify-center h-12 px-8 rounded-full border border-card-border text-foreground font-medium transition-colors hover:bg-card"
            >
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="currentColor"
                className="mr-2"
              >
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
              </svg>
              GitHub
            </a>
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 text-muted/50 animate-bounce">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M7 13l5 5 5-5M7 6l5 5 5-5" />
          </svg>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-32 px-6">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-bold text-center mb-4">
            Warum VoiceTool?
          </h2>
          <p className="text-muted text-center max-w-2xl mx-auto mb-16">
            Keine Cloud. Kein Abo. Keine Kompromisse.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <FeatureCard
              icon={
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <rect width="18" height="18" x="3" y="3" rx="2" />
                  <path d="M7 7h.01M7 12h.01M12 7h.01" />
                </svg>
              }
              title="100% Lokal"
              description="Audio verlässt niemals dein Gerät. Whisper läuft direkt auf dem Neural Engine."
            />
            <FeatureCard
              icon={
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
                </svg>
              }
              title="Unter 1.5 Sekunden"
              description="Optimiert für Apple Silicon. Von Sprechen bis Text in unter 1.5s auf M3."
            />
            <FeatureCard
              icon={
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <rect width="18" height="11" x="3" y="11" rx="2" ry="2" />
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                </svg>
              }
              title="Datenschutz"
              description="Audio wird sofort nach Verarbeitung gelöscht. Keine Logs, keine Speicherung."
            />
            <FeatureCard
              icon={
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <rect width="20" height="14" x="2" y="3" rx="2" />
                  <line x1="8" x2="16" y1="21" y2="21" />
                  <line x1="12" x2="12" y1="17" y2="21" />
                </svg>
              }
              title="Überall einsetzbar"
              description="Funktioniert in jeder App — Safari, Slack, VS Code, Notion, Mail und mehr."
            />
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-32 px-6 border-t border-card-border">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-bold text-center mb-16">
            So funktioniert&apos;s
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <Step
              number="1"
              title="Hotkey halten"
              description="Drücke beide Pfeiltasten gleichzeitig und sprich los. Kein Fenster, kein Klick nötig."
            />
            <Step
              number="2"
              title="Whisper transkribiert"
              description="mlx-whisper erkennt deine Sprache lokal auf dem Neural Engine — blitzschnell."
            />
            <Step
              number="3"
              title="Text erscheint"
              description="Der bereinigte Text wird direkt ins aktive Textfeld eingefügt. Fertig."
            />
          </div>
        </div>
      </section>

      {/* Requirements */}
      <section className="py-32 px-6 border-t border-card-border">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            Voraussetzungen
          </h2>
          <p className="text-muted mb-12">
            VoiceTool läuft auf jedem Mac mit Apple Silicon.
          </p>

          <div className="inline-flex flex-col sm:flex-row gap-6 text-left">
            <Requirement label="macOS" value="Ventura oder neuer" />
            <Requirement label="Chip" value="Apple Silicon (M1+)" />
            <Requirement label="RAM" value="8 GB (16 GB empfohlen)" />
            <Requirement label="Speicher" value="~500 MB für Modell" />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-card-border">
        <div className="max-w-5xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-muted">
          <span>VoiceTool — Voice-Dictation für macOS</span>
          <div className="flex items-center gap-6">
            <a href="https://github.com/sahinelcoder/VoiceTool" className="hover:text-foreground transition-colors">
              GitHub
            </a>
            <span>MIT License</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="flex flex-col p-6 rounded-2xl bg-card border border-card-border transition-colors hover:border-accent/30">
      <div className="w-10 h-10 flex items-center justify-center rounded-lg bg-accent/10 text-accent mb-4">
        {icon}
      </div>
      <h3 className="font-semibold text-lg mb-2">{title}</h3>
      <p className="text-sm text-muted leading-relaxed">{description}</p>
    </div>
  );
}

function Step({
  number,
  title,
  description,
}: {
  number: string;
  title: string;
  description: string;
}) {
  return (
    <div className="flex flex-col items-center text-center">
      <div className="w-12 h-12 flex items-center justify-center rounded-full bg-accent text-white font-bold text-lg mb-4">
        {number}
      </div>
      <h3 className="font-semibold text-lg mb-2">{title}</h3>
      <p className="text-sm text-muted leading-relaxed">{description}</p>
    </div>
  );
}

function Requirement({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center gap-3 px-5 py-3 rounded-xl bg-card border border-card-border">
      <span className="text-xs font-mono text-accent uppercase tracking-wider">
        {label}
      </span>
      <span className="text-sm text-foreground">{value}</span>
    </div>
  );
}
