// worker.js — deploy with `wrangler deploy`
// No API keys. No LLM calls. Just GitHub's public events endpoint + pure logic.
//
// Route: GET /badge.svg?user=<github-username>
//
// Classifies recent commit activity into a "chronotype" (early bird / day shift /
// night owl / vampire hours) purely from public PushEvent timestamps, then renders
// an inline SVG badge. Cached for an hour so it doesn't hammer the GitHub API.

export default {
    async fetch(request) {
        const url = new URL(request.url);
        const user = url.searchParams.get("user") || "octocat";

        const cacheKey = new Request(url.toString(), request);
        const cache = caches.default;
        const cached = await cache.match(cacheKey);
        if (cached) return cached;

        const events = await fetchPublicEvents(user);
        const chronotype = classify(events);
        const svg = renderBadge(chronotype);

        const response = new Response(svg, {
            headers: {
                "Content-Type": "image/svg+xml",
                "Cache-Control": "public, max-age=3600",
            },
        });

        await cache.put(cacheKey, response.clone());
        return response;
    },
};

async function fetchPublicEvents(user) {
    const res = await fetch(`https://api.github.com/users/${user}/events/public`, {
        headers: { "User-Agent": "commit-pulse-badge" },
    });
    if (!res.ok) return [];
    const events = await res.json();
    return events.filter((e) => e.type === "PushEvent");
}

function classify(pushEvents) {
    if (pushEvents.length === 0) {
        return { label: "no recent signal", color: "#778da9" };
    }

    const hourBuckets = { earlyBird: 0, dayShift: 0, nightOwl: 0, vampire: 0 };

    for (const event of pushEvents) {
        const hour = new Date(event.created_at).getUTCHours();
        if (hour >= 5 && hour < 9) hourBuckets.earlyBird++;
        else if (hour >= 9 && hour < 18) hourBuckets.dayShift++;
        else if (hour >= 18 && hour < 24) hourBuckets.nightOwl++;
        else hourBuckets.vampire++;
    }

    const winner = Object.entries(hourBuckets).sort((a, b) => b[1] - a[1])[0][0];

    const labels = {
        earlyBird: { label: "early bird — ships before 9am", color: "#ffd166" },
        dayShift: { label: "day shift — boringly consistent", color: "#06d6a0" },
        nightOwl: { label: "night owl — ships after dark", color: "#118ab2" },
        vampire: { label: "vampire hours — 12am-5am commits", color: "#7209b7" },
    };

    return labels[winner];
}

function renderBadge({ label, color }) {
    const width = 40 + label.length * 7;
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="28">
    <rect width="${width}" height="28" rx="6" fill="#0d1b2a"/>
    <rect x="3" y="3" width="${width - 6}" height="22" rx="4" fill="${color}" opacity="0.15"/>
    <text x="12" y="18" font-family="monospace" font-size="12" fill="${color}">${label}</text>
  </svg>`;
}