import { ButtonLink } from "@/components/ui/Button";

export default function NotFound() {
  return (
    <section className="section">
      <div className="container-x max-w-3xl">
        <p className="eyebrow">Fehler 404</p>
        <h1 className="text-h2 mt-5 font-semibold">Diese Seite gibt es nicht – noch nicht.</h1>
        <p className="mt-5 text-lg text-anthrazit/75">Vielleicht finden Sie das Gesuchte über unsere Leistungen oder Projekte.</p>
        <div className="mt-10 flex flex-wrap gap-3">
          <ButtonLink href="/">Zur Startseite</ButtonLink>
          <ButtonLink href="/leistungen" variant="outline">
            Leistungen
          </ButtonLink>
        </div>
      </div>
    </section>
  );
}
