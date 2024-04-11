import Chart from "react-apexcharts";

export interface AnnualDataset {
  data: number[];
  label: string;
}

export default function AnnualTimeline(props: {
  xAxisCategories: string[];
  datasets: AnnualDataset[];
  title: string;
}): JSX.Element {
  const options: ApexCharts.ApexOptions = {
    stroke: {
      curve: "smooth",
    },
    chart: {
      type: "area",
      fontFamily: "Inter, sans-serif",
      foreColor: "#6B7280",
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    tooltip: {
      style: {
        fontSize: "14px",
        fontFamily: "Inter, sans-serif",
      },
    },
    grid: {
      show: true,
      borderColor: "#F3F4F6",
      strokeDashArray: 1,
      padding: {
        left: 35,
        bottom: 15,
      },
    },
    markers: {
      size: 5,
      strokeColors: "#ffffff",
      hover: {
        size: undefined,
        sizeOffset: 3,
      },
    },
    xaxis: {
      categories: props.xAxisCategories,
      labels: {
        style: {
          colors: ["#6B7280"],
          fontSize: "14px",
          fontWeight: 500,
        },
      },
      axisBorder: {
        color: "#F3F4F6",
      },
      axisTicks: {
        color: "#F3F4F6",
      },
      crosshairs: {
        show: true,
        position: "back",
        stroke: {
          color: "#F3F4F6",
          width: 1,
          dashArray: 10,
        },
      },
    },
    yaxis: {
      labels: {
        style: {
          colors: ["#6B7280"],
          fontSize: "14px",
          fontWeight: 500,
        },
      },
    },
    legend: {
      fontSize: "14px",
      fontWeight: 500,
      fontFamily: "Inter, sans-serif",
      labels: {
        colors: ["#6B7280"],
      },
      itemMargin: {
        horizontal: 10,
      },
    },
    responsive: [
      {
        breakpoint: 1024,
        options: {
          xaxis: {
            labels: {
              show: false,
            },
          },
        },
      },
    ],
  };
  //   const series = [
  //     {
  //       name: "Revenue",
  //       data: [6356, 6218, 6156, 6526, 6356, 6256, 6056],
  //       color: "#1A56DB",
  //     },
  //     {
  //       name: "Profit",
  //       data: [5356, 5218, 5156, 5526, 7356, 4256, 5056],
  //       color: "#307a06",
  //     },
  //   ];

  const series = props.datasets.map((ds) => ({
    name: ds.label,
    data: ds.data,
  }));

  return (
    <div className="rounded-lg bg-white p-2 shadow dark:bg-gray-800 mb-2">
      <div className="px-4 pt-2 mb-2 flex items-center justify-between">
        <div className="shrink-0">
          <span className="text-2xl font-bold leading-none text-gray-900 dark:text-white sm:text-3xl">
            {props.title}
          </span>
          {/* <h3 className="text-base font-normal text-gray-600 dark:text-gray-400">
            Sales this week
          </h3> */}
        </div>
        {/* <div className="flex flex-1 items-center justify-end text-base font-bold text-green-600 dark:text-green-400">
          12.5%
          <svg
            className="h-5 w-5"
            fill="currentColor"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fillRule="evenodd"
              d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z"
              clipRule="evenodd"
            />
          </svg>
        </div> */}
      </div>
      <Chart height={420} options={options} series={series} type="line" />
    </div>
  );
}
