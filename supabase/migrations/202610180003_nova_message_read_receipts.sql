-- Restrict message updates to the read receipt only.
drop policy if exists "Recipients can mark messages read" on public.nova_messages;
revoke update on public.nova_messages from authenticated;
grant update (read_at) on public.nova_messages to authenticated;
create policy "Recipients can mark messages read" on public.nova_messages for update to authenticated
using ((select auth.uid()) = recipient_id)
with check ((select auth.uid()) = recipient_id);
