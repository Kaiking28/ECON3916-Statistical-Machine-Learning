'use client';

import { useState } from 'react';
import Image from 'next/image';

type Thumbnail =
  | { kind: 'single'; src: string; alt: string }
  | { kind: 'double'; src1: string; alt1: string; src2: string; alt2: string }
  | { kind: 'placeholder' };

type GalleryProject = {
  title: string;
  description: string;
  tags: string[];
  thumbnail: Thumbnail;
};

const galleryProjects: GalleryProject[] = [
  {
    title: 'Student Inflation Analysis',
    description:
      'Built a custom Student Price Index tracking rent, tuition, food, and streaming vs official CPI since 2016 using FRED API data. Rent grew 47% — far outpacing national inflation of 34%. Includes regional Boston vs national CPI comparison.',
    tags: ['Python', 'pandas', 'FRED API', 'matplotlib'],
    thumbnail: { kind: 'single', src: '/image4.png', alt: 'Student Inflation chart' },
  },
  {
    title: 'Bias-Variance Tradeoff & Polynomial Regression',
    description:
      'Simulated bias-variance tradeoff on a noisy sine curve (n=50 train, n=200 test, σ=0.3). Fitted degrees 1–15 — test RMSE bottomed at degree 5. Implemented 5-fold CV from scratch. Applied to Ames Housing: 37-feature model (CV RMSE $38,871) outperformed top-5 features ($41,986), confirming low variance costs when n/p ≈ 30.',
    tags: ['Python', 'scikit-learn', 'numpy', 'matplotlib', 'OpenML'],
    thumbnail: { kind: 'single', src: '/image1.png', alt: 'RMSE Training vs Test curve' },
  },
  {
    title: 'Causal Inference & Propensity Score Matching',
    description:
      'Estimated causal effect of a loyalty subscription on customer spending using Propensity Score Matching. Bootstrap confidence intervals on tip distributions, permutation testing with empirical p-value, and Love Plot showing covariate balance before/after PSM. Naive SDO vs corrected PSM ATT comparison.',
    tags: ['Python', 'scikit-learn', 'pandas', 'numpy', 'matplotlib'],
    thumbnail: { kind: 'single', src: '/image2.png', alt: 'Causal Inference chart' },
  },
];

function Thumbnail({ data }: { data: Thumbnail }) {
  if (data.kind === 'single') {
    return (
      <Image
        src={data.src}
        alt={data.alt}
        fill
        className="object-cover"
        sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
      />
    );
  }

  if (data.kind === 'double') {
    return (
      <div className="flex h-full">
        <div className="relative w-1/2 h-full">
          <Image
            src={data.src1}
            alt={data.alt1}
            fill
            className="object-cover"
            sizes="(max-width: 640px) 50vw, (max-width: 1024px) 25vw, 17vw"
          />
        </div>
        <div className="relative w-1/2 h-full border-l border-black/20">
          <Image
            src={data.src2}
            alt={data.alt2}
            fill
            className="object-cover"
            sizes="(max-width: 640px) 50vw, (max-width: 1024px) 25vw, 17vw"
          />
        </div>
      </div>
    );
  }

  return (
    <div className="w-full h-full bg-black flex items-center justify-center">
      <svg
        width={44}
        height={44}
        viewBox="0 0 24 24"
        fill="none"
        stroke="rgba(255,255,255,0.25)"
        strokeWidth={1.5}
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
      >
        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
      </svg>
    </div>
  );
}

export function ProjectGallery() {
  const [activeTag, setActiveTag] = useState('All');

  const allTags = [
    'All',
    ...Array.from(new Set(galleryProjects.flatMap((p) => p.tags))),
  ];

  const visible =
    activeTag === 'All'
      ? galleryProjects
      : galleryProjects.filter((p) => p.tags.includes(activeTag));

  return (
    <section id="gallery">
      {/* Black header band */}
      <div className="bg-black">
        <div className="max-w-5xl mx-auto px-6 py-10">
          <h2 className="text-2xl font-bold tracking-tight text-white">Data Projects</h2>
          <p className="text-neutral-400 text-sm mt-1.5">
            Visualizations and analysis. Hover a card to see key findings.
          </p>
        </div>
      </div>

      {/* White content area */}
      <div className="bg-white dark:bg-neutral-950">
        <div className="max-w-5xl mx-auto px-6 py-12">
          {/* Filter buttons */}
          <div className="flex flex-wrap gap-2 mb-10">
            {allTags.map((tag) => (
              <button
                key={tag}
                onClick={() => setActiveTag(tag)}
                className={
                  tag === activeTag
                    ? 'px-3 py-1.5 rounded-full text-xs font-mono font-medium bg-black dark:bg-white text-white dark:text-black transition-colors'
                    : 'px-3 py-1.5 rounded-full text-xs font-mono font-medium border border-neutral-300 dark:border-neutral-700 text-neutral-500 dark:text-neutral-400 hover:border-black dark:hover:border-white hover:text-black dark:hover:text-white transition-colors'
                }
              >
                {tag}
              </button>
            ))}
          </div>

          {/* Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {visible.map((project) => (
              <article
                key={project.title}
                className="group rounded-xl overflow-hidden border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900 flex flex-col hover:border-black dark:hover:border-neutral-500 transition-colors"
              >
                <div className="relative h-48 bg-neutral-100 dark:bg-neutral-800 overflow-hidden">
                  <Thumbnail data={project.thumbnail} />
                  <div className="absolute inset-0 bg-black/90 opacity-0 group-hover:opacity-100 transition-opacity duration-200 overflow-y-auto p-5">
                    <p className="text-white/85 text-xs leading-relaxed">{project.description}</p>
                  </div>
                </div>

                <div className="p-4 flex flex-col gap-3">
                  <h3 className="font-semibold text-sm text-black dark:text-white leading-snug tracking-tight">
                    {project.title}
                  </h3>
                  <div className="flex flex-wrap gap-1.5">
                    {project.tags.map((tag) => (
                      <span
                        key={tag}
                        className="px-2 py-0.5 rounded-full text-xs font-mono font-medium bg-black dark:bg-white text-white dark:text-black"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </article>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
