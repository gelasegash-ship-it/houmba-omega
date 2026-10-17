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

  // Supabase verifies the JWT at the gateway (verify_jwt=true). This handler deliberately
  // provides a safe planning baseline until a server-side model provider secret is configured.
  let input: { goal?: unknown; constraints?: unknown };
  try { input = await req.json(); } catch { return reply({ error: "Invalid JSON" }, 400); }
  if (typeof input.goal !== "string" || input.goal.trim().length < 3 || input.goal.length > 2000) {
    return reply({ error: "goal must be a string between 3 and 2000 characters" }, 400);
  }
  const constraints = typeof input.constraints === "string" ? input.constraints.slice(0, 2000) : "";
  const plan = [
    { step: 1, title: "Clarify the outcome", detail: "Define a measurable result and a deadline.", approval_required: false },
    { step: 2, title: "Choose the smallest test", detail: "Prefer a low-cost reversible experiment.", approval_required: false },
    { step: 3, title: "Prepare the materials", detail: "Create the offer and the required assets.", approval_required: false },
    { step: 4, title: "Request authorization", detail: "Get approval before contacting people, publishing, spending or changing production systems.", approval_required: true },
    { step: 5, title: "Verify evidence", detail: "Record only outcomes confirmed by a connected source.", approval_required: false },
  ];
  return reply({
    mode: "safe-planning-baseline",
    connected_model: false,
    goal: input.goal.trim(),
    constraints,
    plan,
    notice: "No external action was performed. Configure a server-side model provider and tool adapters to enable AI execution."
  }, 200);
});

function reply(body: unknown, status: number) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders, "Content-Type": "application/json; charset=utf-8" },
  });
}
