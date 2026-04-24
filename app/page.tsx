import { Mail } from 'lucide-react';
import Image from 'next/image';
import { ThemeToggle } from './components/ThemeToggle';
import { ProjectGallery } from './components/ProjectGallery';

function GitHubIcon({ size = 18, className = '' }: { size?: number; className?: string }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="currentColor"
      aria-hidden="true"
      className={className}
    >
      <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0 1 12 6.844a9.59 9.59 0 0 1 2.504.337c1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.02 10.02 0 0 0 22 12.017C22 6.484 17.522 2 12 2z" />
    </svg>
  );
}

function SectionHeader({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div className="bg-black">
      <div className="max-w-5xl mx-auto px-6 py-10">
        <h2 className="text-2xl font-bold tracking-tight text-white">{title}</h2>
        <p className="text-neutral-400 text-sm mt-1.5">{subtitle}</p>
      </div>
    </div>
  );
}

const projects = [
  {
    title: 'Sovereign Risk & Economic Crisis Prediction',
    description:
      'Built Ridge and Lasso regularization models to predict GDP growth and classify economic crises across 100+ countries using 35 World Bank indicators. Demonstrated OLS overfitting with high p/n ratio and used cross-validated regularization to improve out-of-sample performance.',
    tech: ['Python', 'scikit-learn', 'pandas', 'statsmodels', 'wbgapi', 'seaborn'],
    href: 'https://github.com/Kaiking28',
  },
  {
    title: 'Healthcare Cost Modeling & Causal Inference',
    description:
      'Analyzed OmniCare clinical and telemetry data to model procedure costs. Addressed multicollinearity via VIF analysis, handled MNAR missing data, applied target encoding for high-cardinality diagnosis codes, and diagnosed heteroscedasticity in residuals.',
    tech: ['Python', 'statsmodels', 'pandas', 'seaborn', 'category-encoders'],
    href: 'https://github.com/Kaiking28',
  },
  {
    title: 'Causal Inference & Propensity Score Matching',
    description:
      'Estimated the causal effect of a loyalty subscription program on customer spending using propensity score matching. Removed selection bias by matching on pre-treatment spending, account age, and support tickets. Compared naive SDO to PSM ATT estimates.',
    tech: ['Python', 'scikit-learn', 'pandas', 'numpy', 'matplotlib'],
    href: 'https://github.com/Kaiking28',
  },
];

const skillGroups: Record<string, string[]> = {
  Languages: ['Python', 'R', 'SQL', 'JavaScript'],
  'Libraries & ML': ['Pandas', 'Matplotlib', 'scikit-learn', 'statsmodels', 'Jupyter'],
  'Tools & Platforms': ['Git', 'FRED API', 'Tableau', 'Power BI'],
};

export default function Home() {
  return (
    <>
      {/* Navbar — always black */}
      <header className="sticky top-0 z-50 bg-black border-b border-neutral-800">
        <nav className="max-w-5xl mx-auto px-6 h-14 flex items-center justify-between">
          <span className="font-semibold text-sm text-white tracking-tight">
            Kai Kagawa King
          </span>
          <div className="flex items-center gap-6">
            <div className="hidden sm:flex gap-6 text-sm text-white/50">
              <a href="#projects" className="hover:text-white transition-colors">Projects</a>
              <a href="#gallery" className="hover:text-white transition-colors">Gallery</a>
              <a href="#skills" className="hover:text-white transition-colors">Skills</a>
              <a href="#contact" className="hover:text-white transition-colors">Contact</a>
            </div>
            <ThemeToggle />
          </div>
        </nav>
      </header>

      <main>
        {/* Hero */}
        <section className="relative bg-white dark:bg-neutral-950 overflow-hidden">
          <div className="absolute inset-0">
            <Image
              src="/Boston_skyline_shutterstock_433157269_1110x460.webp"
              alt="Boston skyline"
              fill
              className="object-cover object-center"
              priority
            />
            <div className="absolute inset-0 bg-black/60" />
          </div>
          <div className="relative max-w-5xl mx-auto px-6 py-24 sm:py-32">
            <div className="flex flex-col-reverse sm:flex-row items-center gap-12">
              <div className="flex-1">
                <p className="text-neutral-300 text-sm font-medium mb-4 tracking-wide">
                  B.S. Data Science &amp; Economics · Minor in Mathematics · Northeastern University
                </p>
                <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-white mb-6">
                  Kai Kagawa King
                </h1>
                <p className="text-lg text-neutral-200 leading-relaxed mb-8">
                  Data Science &amp; Economics student at Northeastern University with experience in
                  econometrics, machine learning, and policy analysis.
                </p>
                <div className="flex flex-wrap gap-3">
                  <a
                    href="mailto:king.kai@northeastern.edu"
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white text-black text-sm font-medium hover:bg-neutral-100 transition-colors"
                  >
                    <Mail size={15} />
                    Email me
                  </a>
                  <a
                    href="https://github.com/Kaiking28"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white text-white text-sm font-medium hover:bg-white hover:text-black transition-colors"
                  >
                    <GitHubIcon size={15} />
                    GitHub
                  </a>
                </div>
              </div>
              <div className="shrink-0">
                <Image
                  src="/profile.png"
                  alt="Kai Kagawa King"
                  width={192}
                  height={192}
                  className="rounded-full object-cover ring-2 ring-white/40"
                  priority
                />
              </div>
            </div>
          </div>
        </section>

        {/* Projects */}
        <section id="projects">
          <SectionHeader title="Projects" subtitle="Selected research and data science work." />
          <div className="bg-white dark:bg-neutral-950">
            <div className="max-w-5xl mx-auto px-6 py-12">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {projects.map((project) => (
                  <div
                    key={project.title}
                    className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl p-6 flex flex-col gap-4 hover:border-black dark:hover:border-neutral-500 transition-colors"
                  >
                    <h3 className="font-semibold text-black dark:text-white leading-snug">
                      {project.title}
                    </h3>
                    <p className="text-neutral-600 dark:text-neutral-400 text-sm leading-relaxed flex-1">
                      {project.description}
                    </p>
                    <div className="flex flex-wrap gap-1.5">
                      {project.tech.map((t) => (
                        <span
                          key={t}
                          className="px-2 py-0.5 rounded-full bg-black dark:bg-white text-white dark:text-black text-xs font-medium font-mono"
                        >
                          {t}
                        </span>
                      ))}
                    </div>
                    <a
                      href={project.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1.5 text-neutral-400 dark:text-neutral-500 text-sm hover:text-black dark:hover:text-white transition-colors w-fit"
                    >
                      <GitHubIcon size={14} />
                      View on GitHub
                    </a>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <ProjectGallery />

        {/* Skills */}
        <section id="skills">
          <SectionHeader title="Skills" subtitle="Technologies and tools I work with." />
          <div className="bg-white dark:bg-neutral-950">
            <div className="max-w-5xl mx-auto px-6 py-12">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-10">
                {Object.entries(skillGroups).map(([group, items]) => (
                  <div key={group}>
                    <h3 className="text-xs font-semibold uppercase tracking-wider text-neutral-400 mb-3">
                      {group}
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {items.map((skill) => (
                        <span
                          key={skill}
                          className="px-3 py-1.5 rounded-lg bg-black dark:bg-white text-white dark:text-black text-sm font-medium font-mono"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Contact */}
        <section id="contact">
          <SectionHeader
            title="Contact"
            subtitle="Open to research collaborations, internships, and opportunities."
          />
          <div className="bg-white dark:bg-neutral-950">
            <div className="max-w-5xl mx-auto px-6 py-12">
              <div className="flex flex-col sm:flex-row gap-4">
                <a
                  href="mailto:king.kai@northeastern.edu"
                  className="inline-flex items-center gap-4 px-5 py-4 rounded-xl border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900 hover:border-black dark:hover:border-white transition-colors group"
                >
                  <Mail size={20} className="text-black dark:text-white shrink-0" />
                  <div>
                    <div className="text-xs text-neutral-400 mb-0.5 font-medium uppercase tracking-wide">
                      Email
                    </div>
                    <div className="text-sm font-medium text-neutral-600 dark:text-neutral-400 group-hover:text-black dark:group-hover:text-white transition-colors">
                      king.kai@northeastern.edu
                    </div>
                  </div>
                </a>
                <a
                  href="https://github.com/Kaiking28"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-4 px-5 py-4 rounded-xl border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900 hover:border-black dark:hover:border-white transition-colors group"
                >
                  <GitHubIcon size={20} className="text-black dark:text-white shrink-0" />
                  <div>
                    <div className="text-xs text-neutral-400 mb-0.5 font-medium uppercase tracking-wide">
                      GitHub
                    </div>
                    <div className="text-sm font-medium text-neutral-600 dark:text-neutral-400 group-hover:text-black dark:group-hover:text-white transition-colors">
                      github.com/Kaiking28
                    </div>
                  </div>
                </a>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer — always black */}
      <footer className="bg-black border-t border-neutral-800">
        <div className="max-w-5xl mx-auto px-6 py-6 flex flex-col sm:flex-row items-center justify-between gap-2 text-sm text-white/40">
          <span>© 2025 Kai Kagawa King</span>
          <span>B.S. Data Science &amp; Economics — Northeastern University</span>
        </div>
      </footer>
    </>
  );
}
