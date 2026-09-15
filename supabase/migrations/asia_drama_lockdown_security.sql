-- Security hardening for sensitive business data.
revoke all on public.admin_roles from anon, authenticated;
revoke all on public.audit_logs from anon, authenticated;
revoke all on public.payment_webhook_events from anon, authenticated;
revoke all on public.payment_transactions from anon;
revoke all on public.entitlements from anon;
revoke all on public.orders from anon;
revoke all on public.order_items from anon;
revoke all on public.user_subscriptions from anon;
revoke all on public.watch_history from anon;
revoke execute on function public.has_admin_access(uuid) from anon, authenticated;
revoke execute on function public.can_watch_episode(uuid,uuid) from anon, authenticated;
grant execute on function public.can_watch_episode(uuid,uuid) to authenticated;
grant execute on function public.grant_admin_entitlement(uuid,uuid,uuid,uuid,timestamptz,text) to authenticated;