import { useEffect, useState } from "react";
import StyledTable from "../components/StyledTable";
import {
  AnnualInfo,
  AnnualInfoMap,
  DistrictInfo,
  EventType,
  QualRecordClass,
  TeamEvent,
} from "../types";
import useDataStore from "../store";

const emptyRecord: QualRecordClass = { won: 0, lost: 0, tied: 0 };

function countDCMPs(
  teamKey: string,
  activeYears: number[],
  annualInfos: AnnualInfoMap
): number {
  return activeYears.filter(
    (y) =>
      annualInfos[y.toString()].team_events[teamKey].filter(
        (e) =>
          e.event_type === EventType.DISTRICT_CMP ||
          e.event_type === EventType.DISTRICT_CMP_DIVISION
      ).length > 0
  ).length;
}

export default function District(props: { districtKey: string }): JSX.Element {
  const { data, fetchData } = useDataStore();

  useEffect(() => {
    console.log("umm");
    // Example usage of fetchData method with fetch
    const fetchDataFromUrl = async () => {
      try {
        // Call fetchData with a unique key and the URL to fetch data from
        await fetchData(
          props.districtKey,
          `district/${props.districtKey}/annual_infos`
        );
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchDataFromUrl();
  }, [fetchData, props.districtKey]); // Make sure to include fetchData in the dependency array to avoid linting warning

  const [activeOnly, setActiveOnly] = useState(true);

  if (!Object.hasOwn(data, props.districtKey)) {
    return <>loading...</>;
  }

  const info = data![props.districtKey];

  const sortedTeams = Object.values(info.summary.all_teams);
  sortedTeams.sort((a, b) => a.number - b.number);

  return (
    <>
      <section className="bg-white dark:bg-gray-900">
        <div className="pt-8 px-4 mx-auto max-w-screen-xl text-center">
          <h1 className="text-4xl font-extrabold tracking-tight leading-none text-gray-900 md:text-5xl lg:text-6xl dark:text-white">
            {info.summary.name}
          </h1>
        </div>
      </section>

      <div className="p-2 bg-white rounded-lg md:p-2 dark:bg-gray-800">
        <dl className="grid max-w-screen-xl grid-cols-4 gap-8 p-4 mx-auto text-gray-900 dark:text-white sm:p-8">
          <div className="flex flex-col items-center justify-center">
            <dt className="mb-2 text-3xl font-extrabold">
              {info.summary.first_year}
            </dt>
            <dd className="text-gray-500 dark:text-gray-400">First Year</dd>
          </div>
          <div className="flex flex-col items-center justify-center">
            <dt className="mb-2 text-3xl font-extrabold">
              {sortedTeams.length}
            </dt>
            <dd className="text-gray-500 dark:text-gray-400">all-time teams</dd>
          </div>
          <div className="flex flex-col items-center justify-center">
            <dt className="mb-2 text-3xl font-extrabold">
              {sortedTeams.filter((t) => t.active_years.includes(2024)).length}
            </dt>
            <dd className="text-gray-500 dark:text-gray-400">active teams</dd>
          </div>
          <div className="flex flex-col items-center justify-center">
            <dt className="mb-2 text-3xl font-extrabold">
              {Object.values(info.annual_info)
                .map((ai) => ai.events.length)
                .reduce((prev, curr) => prev + curr, 0)}
            </dt>
            <dd className="text-gray-500 dark:text-gray-400">events</dd>
          </div>
        </dl>
      </div>

      <label className="inline-flex items-center cursor-pointer">
        <input
          type="checkbox"
          value=""
          className="sr-only peer"
          checked={activeOnly}
          onChange={(e) => setActiveOnly(e.target.checked)}
        />
        <div className="relative w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
        <span className="ms-3 text-sm font-medium text-gray-900 dark:text-gray-300">
          Active Teams Only
        </span>
      </label>

      <StyledTable
        columns={[
          {
            header: "\xa0",
            accessorFn: (t) => t.active_years.includes(2024),
            cell(props) {
              return (props.getValue() as boolean) ? (
                <span className="flex w-3 h-3 me-3 bg-green-500 rounded-full"></span>
              ) : (
                <span className="flex w-3 h-3 me-3 bg-red-500 rounded-full"></span>
              );
            },
            size: 1,
          },
          { header: "#", accessorFn: (t) => t.number, size: 25 },
          { header: "Name", accessorFn: (t) => t.name, size: 200 },
          {
            header: "Location",
            accessorFn: (t) => `${t.city}, ${t.state_prov}`,
            size: 300,
          },
          {
            header: "Seasons",
            accessorFn: (t) => t.active_years.length,
            size: 75,
          },
          {
            header: "DCMPs",
            accessorFn: (t) =>
              countDCMPs(t.key, t.active_years, info.annual_info),
            size: 75,
          },
          {
            header: "DCMP %",
            accessorFn: (t) =>
              `${(
                (100 * countDCMPs(t.key, t.active_years, info.annual_info)) /
                t.active_years.length
              ).toFixed(0)}%`,
            size: 100,
          },
          {
            header: "Matches",
            accessorFn: (t) =>
              t.active_years
                .map((y) =>
                  info.annual_info[y].team_events[t.key]
                    .map((te) => te.match_keys.length)
                    .reduce((p, c) => p + c, 0)
                )
                .reduce((p, c) => p + c, 0),
            size: 75,
          },
          {
            header: "Record",
            accessorFn: (t) => {
              const record = t.active_years
                .map((y) =>
                  info.annual_info[y].team_events[t.key]
                    .map((te) => te.total_record)
                    .reduce(
                      (p, c) => ({
                        won: (p || emptyRecord).won + (c || emptyRecord).won,
                        lost: (p || emptyRecord).lost + (c || emptyRecord).lost,
                        tied: (p || emptyRecord).tied + (c || emptyRecord).tied,
                      }),
                      {
                        won: 0,
                        lost: 0,
                        tied: 0,
                      } as QualRecordClass
                    )
                )
                .reduce(
                  (p, c) => ({
                    won: (p || emptyRecord).won + (c || emptyRecord).won,
                    lost: (p || emptyRecord).lost + (c || emptyRecord).lost,
                    tied: (p || emptyRecord).tied + (c || emptyRecord).tied,
                  }),
                  {
                    won: 0,
                    lost: 0,
                    tied: 0,
                  } as QualRecordClass
                );

              if (record?.tied === 0) {
                return `${record?.won}-${record?.lost}`;
              }

              return `${record?.won}-${record?.lost}-${record?.tied}`;
            },
            size: 125,
          },
        ]}
        data={sortedTeams.filter((t) =>
          activeOnly ? t.active_years.includes(2024) : true
        )}
      />
    </>
  );
}
