import { InputWebLink } from "./components/ui/InputWebLink/InputWebLink";

export default function Home() {
  return (
    <main className="min-h-screen bg-navy-dark">
      <div className="container mx-auto pt-8">
        <h1 className="text-4xl font-bold text-center text-neutral-50 mb-8">
          Analyze Your Website
        </h1>
        <InputWebLink />
      </div>
    </main>
  );
}
