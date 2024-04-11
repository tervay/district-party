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
import { useDistrictIndexStore } from "../store";
import Chart from "react-apexcharts";
import AreaChart from "../components/AreaChart";
import AnnualTimeline, { AnnualDataset } from "../components/AnnualTimeline";
import { Select } from "flowbite-react";
import { CURRENT_YEAR } from "../consts";

const OVERALL_RANKINGS_KEY = "Overall";

export default function District(props: { districtKey: string }): JSX.Element {
  const { data, fetchData } = useDistrictIndexStore();

  useEffect(() => {
    const fetchDataFromUrl = async () => {
      try {
        await fetchData(props.districtKey, `d/${props.districtKey}`);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchDataFromUrl();
  }, [fetchData, props.districtKey]);

  const [rankingsYear, setRankingsYear] = useState(OVERALL_RANKINGS_KEY);

  if (!Object.hasOwn(data, props.districtKey)) {
    return <>loading...</>;
  }

  const info = data[props.districtKey]!;

  const stateSet: Set<string> = new Set(
    Object.keys(info.teams_per_year).flatMap((year) =>
      Object.keys(info.teams_per_year[year])
    )
  );
  const datasets: AnnualDataset[] = [];
  stateSet.forEach((s) => {
    datasets.push({
      data: Object.keys(info.teams_per_year).map(
        (y) => info.teams_per_year[y][s] ?? null
      ),
      label: s,
    });
  });
  datasets.push({
    label: "Total",
    data: Object.values(info.teams_per_year).map((stateBreakdown) =>
      Object.values(stateBreakdown).reduce((p, c) => p + c, 0)
    ),
  });

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
        <dl className="grid max-w-screen-xl grid-cols-5 gap-8 p-4 mx-auto text-gray-900 dark:text-white sm:p-8">
          <div className="flex flex-col items-center justify-center">
            <dt className="mb-2 text-3xl font-extrabold">
              {Object.values(info.summary.all_teams).length}
            </dt>
            <dd className="text-gray-500 dark:text-gray-400">all-time teams</dd>
          </div>
          <div className="flex flex-col items-center justify-center">
            <dt className="mb-2 text-3xl font-extrabold">
              {
                Object.values(info.summary.all_teams).filter((t) =>
                  t.active_years.includes(CURRENT_YEAR)
                ).length
              }
            </dt>
            <dd className="text-gray-500 dark:text-gray-400">active teams</dd>
          </div>
          <div className="flex flex-col items-center justify-center">
            <dt className="mb-2 text-3xl font-extrabold">
              {info.summary.first_year}
            </dt>
            <dd className="text-gray-500 dark:text-gray-400">First Year</dd>
          </div>
          <div className="flex flex-col items-center justify-center">
            <dt className="mb-2 text-3xl font-extrabold">
              {info.events.recent}
            </dt>
            <dd className="text-gray-500 dark:text-gray-400">
              events in {CURRENT_YEAR}
            </dd>
          </div>
          <div className="flex flex-col items-center justify-center">
            <dt className="mb-2 text-3xl font-extrabold">
              {info.events.total}
            </dt>
            <dd className="text-gray-500 dark:text-gray-400">
              all-time events
            </dd>
          </div>
        </dl>
      </div>

      <AnnualTimeline
        xAxisCategories={Object.keys(info.teams_per_year)}
        datasets={datasets}
        title="Team Growth"
      />

      <div className="flex flex-row w-full">
        <div className="basis-1/4">
          <div className="w-full max-w-sm p-2 bg-white border border-gray-200 rounded-lg shadow sm:p-8 dark:bg-gray-800 dark:border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h5 className="text-xl font-bold leading-none text-gray-900 dark:text-white">
                Rankings
              </h5>
              <a
                href="#"
                className="text-sm font-medium text-blue-600 hover:underline dark:text-blue-500"
              >
                View all
              </a>
            </div>
            <div>
              <Select onChange={(e) => setRankingsYear(e.target.value)}>
                <option>{OVERALL_RANKINGS_KEY}</option>
                {Object.keys(info.rankings.by_year)
                  .reverse()
                  .map((k) => (
                    <option>{k}</option>
                  ))}
              </Select>
              <table className="w-full table-auto text-sm text-left">
                <thead className="text-xs dark:text-gray-400">
                  <tr>
                    <th scope="col" className="w-1/3 px-2 py-3 text-center">
                      Rank
                    </th>
                    <th scope="col" className="w-1/3 px-2 py-3 text-center">
                      Team
                    </th>
                    <th scope="col" className="w-1/3 px-2 py-3 text-center">
                      {rankingsYear === OVERALL_RANKINGS_KEY
                        ? "Avg Pts"
                        : "Pts"}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {(rankingsYear === OVERALL_RANKINGS_KEY
                    ? info.rankings.overall.sort(
                        (b, a) =>
                          a.dcmp_points +
                          a.qualifying_points_total -
                          (b.dcmp_points + b.qualifying_points_total)
                      )
                    : info.rankings.by_year[rankingsYear]
                  ).map((r, i) => (
                    <tr>
                      <th className="text-center">
                        {rankingsYear === OVERALL_RANKINGS_KEY ? i + 1 : r.rank}
                      </th>
                      <td className="text-center">{r.team_key.substring(3)}</td>
                      <td className="text-center">
                        {(r.qualifying_points_total + r.dcmp_points).toFixed(0)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div className="basis-1/2"></div>
        <div className="basis-1/4 h-full  block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow">
          <h5 className="mb-2 text-center text-2xl font-bold text-gray-900">
            DCMP Winners
          </h5>
          {info.winners
            .sort((a, b) => b.year - a.year)
            .map((w) => (
              <dl className="grid grid-cols-4 p-1.5 mx-auto text-gray-900">
                <div className="flex flex-col items-center justify-center">
                  <dt className="mb-1 text-xl font-bold">{w.year}</dt>
                </div>
                {w.teams.map((t) => (
                  <div className="flex flex-col items-center justify-center">
                    <dt className="mb-1 text-xl">{t.substring(3)}</dt>
                  </div>
                ))}
              </dl>
            ))}
        </div>
      </div>

      {/* <label className="inline-flex items-center cursor-pointer">
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
      </label> */}

      {/* <StyledTable
        columns={[
          {
            header: "\xa0",
            accessorFn: (t) => t.team.active_years.includes(2024),
            cell(props) {
              return (props.getValue() as boolean) ? (
                <span className="flex w-3 h-3 me-3 bg-green-500 rounded-full"></span>
              ) : (
                <span className="flex w-3 h-3 me-3 bg-red-500 rounded-full"></span>
              );
            },
            size: 1,
          },
          { header: "#", accessorFn: (t) => t.team.number, size: 25 },
          { header: "Name", accessorFn: (t) => t.team.name, size: 200 },
          {
            header: "Location",
            accessorFn: (t) => `${t.team.city}, ${t.team.state_prov}`,
            size: 300,
          },
          {
            header: "Seasons",
            accessorFn: (t) => t.team.active_years.length,
            size: 75,
          },
          {
            header: "DCMPs",
            accessorFn: (t) => t.dcmps,
            size: 75,
          },
          {
            header: "DCMP %",
            accessorFn: (t) =>
              `${((100 * t.dcmps) / t.team.active_years.length).toFixed(0)}%`,
            size: 100,
            sortingFn: (rowA, rowB, columnID) => {
              const b = parseInt(
                (rowB.getValue(columnID) as string).replace("%", "")
              );
              const a = parseInt(
                (rowA.getValue(columnID) as string).replace("%", "")
              );

              if (a < b) {
                return -1;
              }
              if (a === b) {
                return 0;
              }
              if (a > b) {
                return 1;
              }

              return 0;
            },
          },
          {
            header: "Matches",
            accessorFn: (t) => t.record.wins + t.record.losses + t.record.ties,
            size: 75,
          },
          {
            header: "Record",
            accessorFn: (t) =>
              `${t.record.wins}-${t.record.losses}` +
              (t.record.ties === 0 ? "" : `-${t.record.ties}`),
            size: 125,
          },
          {
            header: "EPA",
            accessorFn: (t) => t.epa,
          },
        ]}
        data={info.team_data.filter((t) =>
          activeOnly ? t.team.active_years.includes(2024) : true
        )}
      /> */}
    </>
  );
}
