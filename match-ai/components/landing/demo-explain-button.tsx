"use client";

import { Info } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Dialog } from "@/components/ui/dialog";
import { useMessages } from "@/hooks/use-messages";

export function DemoExplainButton() {
  const [open, setOpen] = useState(false);
  const demo = useMessages().landing.demo;
  return (
    <>
      <Button variant="ghost" size="sm" onClick={() => setOpen(true)} aria-haspopup="dialog">
        <Info aria-hidden="true" />
        {demo.explainButton}
      </Button>
      <Dialog open={open} onOpenChange={setOpen} title={demo.explainTitle} description={demo.explainBody} />
    </>
  );
}
