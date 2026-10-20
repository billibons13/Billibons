import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { Suspense } from "react";
import { CalendarDays, CreditCard, LogOut } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button, ButtonLink } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Container } from "@/components/ui/container";
import { Skeleton } from "@/components/ui/skeleton";
import { signOutAction } from "@/lib/auth/actions";
import { getCurrentUser } from "@/lib/auth/session";
import { PLAN_IDS, getPlan, type PlanId } from "@/lib/config/plans";
import { createSupabaseServerClient } from "@/lib/db/server";
import { format, getMessages } from "@/lib/i18n";

const m = getMessages();

export const metadata: Metadata = { title: m.dashboard.metaTitle, robots: { index: false } };

async function getPlanId(userId: string): Promise<PlanId> {
  const supabase = await createSupabaseServerClient();
  if (!supabase) return "free";
  const { data } = await supabase.from("profiles").select("plan_id").eq("id", userId).maybeSingle();
  const value = (data as { plan_id?: string } | null)?.plan_id;
  return (PLAN_IDS as readonly string[]).includes(value ?? "") ? (value as PlanId) : "free";
}

async function DashboardContent() {
  const user = await getCurrentUser();
  if (!user) redirect("/login");

  const d = m.dashboard;
  const planId = await getPlanId(user.id);
  const plan = getPlan(planId);
  const planName = m.landing.pricing.plans[planId].name;
  const memberSince = user.createdAt
    ? new Intl.DateTimeFormat("en", { dateStyle: "long" }).format(new Date(user.createdAt))
    : null;

  return (
    <>
      <h1 className="font-display text-3xl font-semibold tracking-tight sm:text-4xl">{d.welcome}</h1>
      <p className="mt-2 break-all text-muted">{format(d.signedInAs, { email: user.email ?? "—" })}</p>

      <div className="mt-10 grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardDescription className="flex items-center gap-2">
              <CreditCard className="size-4" aria-hidden="true" />
              {d.planTitle}
            </CardDescription>
            <CardTitle className="flex items-center gap-2 text-2xl">
              {format(d.planName, { plan: planName })}
              {plan.highlighted ? <Badge variant="accent">{m.landing.pricing.popular}</Badge> : null}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted">{format(d.usageLabel, { count: plan.analysesPerMonth })}</p>
            <ButtonLink href="/#pricing" variant="secondary" size="sm" className="mt-5">
              {d.viewPlans}
            </ButtonLink>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardDescription className="flex items-center gap-2">
              <CalendarDays className="size-4" aria-hidden="true" />
              {d.accountTitle}
            </CardDescription>
            <CardTitle className="break-all text-lg">{user.email}</CardTitle>
          </CardHeader>
          <CardContent>
            {memberSince ? <p className="text-sm text-muted">{format(d.memberSince, { date: memberSince })}</p> : null}
            <form action={signOutAction} className="mt-5">
              <Button type="submit" variant="ghost" size="sm">
                <LogOut aria-hidden="true" />
                {d.signOut}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </>
  );
}

function DashboardSkeleton() {
  return (
    <div aria-busy="true" aria-label={m.dashboard.loadingAccount}>
      <Skeleton className="h-10 w-56" />
      <Skeleton className="mt-3 h-5 w-72 max-w-full" />
      <div className="mt-10 grid gap-4 md:grid-cols-2">
        <Skeleton className="h-48 rounded-2xl" />
        <Skeleton className="h-48 rounded-2xl" />
      </div>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <Container className="max-w-4xl py-14 sm:py-20">
      <Suspense fallback={<DashboardSkeleton />}>
        <DashboardContent />
      </Suspense>
    </Container>
  );
}
