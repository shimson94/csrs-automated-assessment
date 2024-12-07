<<<<<<< HEAD
import { redirect } from 'next/navigation';

export default function Home() {
  redirect('/dashboard');
=======
export default function Home() {
  return (
    <main><h1>Hello world</h1></main>
  );
>>>>>>> 0d3f037 (Populate dashboard and add pages for assessments, marking-suite and submissions)
}
