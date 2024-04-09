import useDataStore from "./store";
import { Link } from "wouter";

export default function Landing(): JSX.Element {
  return (
    <div>
      landing
      {/* {Object.keys(data!).map((key) => (
        <Link href={`/district/${key}`}>
          <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
            {key}
          </h5>
        </Link>
      ))} */}
    </div>
  );
}
