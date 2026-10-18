import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": Deno.env.get("NOVA_ALLOWED_ORIGIN") ?? "https://gelasegash-ship-it.github.io",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
  if (req.method !== "POST") return reply({ error: "Method not allowed" }, 405);
  const auth = req.headers.get("Authorization");
  if (!auth?.startsWith("Bearer ")) return reply({ error: "Authentication required" }, 401);

  let input: { goal?: unknown; constraints?: unknown };
  try { input = await req.json(); } catch { return reply({ error: "Invalid JSON" }, 400); }
  if (typeof input.goal !== "string" || input.goal.trim().length < 3 || input.goal.length > 2000) {
    return reply({ error: "goal must be a string between 3 and 2000 characters" }, 400);
  }
  const goal = input.goal.trim();
  const constraints = typeof input.constraints === "string" ? input.constraints.slice(0, 2000) : "";
  const apiKey = Deno.env.get("OPENAI_API_KEY");

  // A real model is used only when its server-side secret is configured.
  // Never place OPENAI_API_KEY in the browser or in the repository.
  if (apiKey) {
    try {
      const response = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: { "Authorization": `Bearer ${apiKey}`, "Content-Type": "application/json" },
        body: JSON.stringify({
          model: Deno.env.get("OPENAI_MODEL") ?? "gpt-4o-mini",
          temperature: 0.3,
          response_format: { type: "json_object" },
          messages: [
            { role: "system", content: "Tu es NOVA CORE, assistant de planification prudent. Réponds en français. N'invente jamais de revenus, résultats ou faits. Ne prétends pas exécuter des actions externes. Pour toute dépense, publication, contact, transfert ou action irréversible, demande une validation humaine. Retourne un objet JSON avec un tableau plan de 4 à 7 éléments, chaque élément ayant step (nombre), title (texte), detail (texte), approval_required (booléen). Inclus une notice honnête." },
            { role: "user", content: JSON.stringify({ goal, constraints }) }
          ]
        })
      });
      if (!response.ok) throw new Error(`Model provider HTTP ${response.status}`);
      const payload = await response.json();
      const raw = payload?.choices?.[0]?.message?.content;
      if (typeof raw !== "string") throw new Error("Empty model response");
      const parsed = JSON.parse(raw);
      if (!Array.isArray(parsed.plan) || parsed.plan.length < 1 || parsed.plan.length > 10) throw new Error("Invalid plan schema");
      return reply({
        mode: "openai-planning",
        connected_model: true,
        goal,
        constraints,
        plan: parsed.plan.map((p: any, i: number) => ({
          step: Number.isFinite(p.step) ? p.step : i + 1,
          title: String(p.title ?? "Étape").slice(0, 160),
          detail: String(p.detail ?? "").slice(0, 1000),
          approval_required: Boolean(p.approval_required)
        })),
        notice: typeof parsed.notice === "string" ? parsed.notice.slice(0, 1000) : "Plan généré par le modèle; vérifie-le avant d'agir."
      }, 200);
    } catch (error) {
      console.error("Model planning failed; falling back to baseline:", error);
      // Safe fallback below: the endpoint remains useful during provider outages.
    }
  }

  const plan = [
    { step: 1, title: "Clarifier le résultat", detail: "Définis un résultat mesurable et une échéance réaliste.", approval_required: false },
    { step: 2, title: "Choisir le plus petit test", detail: "Privilégie une expérience réversible et peu coûteuse.", approval_required: false },
    { step: 3, title: "Préparer les supports", detail: "Crée une offre claire et les éléments nécessaires.", approval_required: false },
    { step: 4, title: "Demander l'autorisation", detail: "Obtiens l'accord avant de contacter des personnes, publier, dépenser ou modifier la production.", approval_required: true },
    { step: 5, title: "Vérifier les preuves", detail: "Enregistre uniquement les résultats confirmés par une source fiable.", approval_required: false },
  ];
  return reply({
    mode: "safe-planning-baseline",
    connected_model: false,
    goal,
    constraints,
    plan,
    notice: apiKey
      ? "Le fournisseur IA n'a pas répondu correctement; plan de base utilisé."
      : "Aucune clé OPENAI_API_KEY n'est configurée côté serveur. Plan de base utilisé; aucune action externe n'a été effectuée."
  }, 200);
});

function reply(body: unknown, status: number) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders, "Content-Type": "application/json; charset=utf-8" },
  });
}
