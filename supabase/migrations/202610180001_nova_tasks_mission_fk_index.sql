-- Cover the mission foreign key for efficient joins and cascades.
create index if not exists nova_tasks_mission_id_idx on public.nova_tasks(mission_id);
