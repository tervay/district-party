import { create } from "zustand";
import { DistrictInfoMap } from "./types";
import { DistrictIndexData } from "./district/index_types";

interface DataStore {
  data: DistrictInfoMap; // Change 'any' to the type of your JSON data
  isLoading: { [key: string]: boolean };
  error: { [key: string]: string | null | undefined };
  fetchData: (key: string, url: string) => Promise<void>;
}

function makeStore<T>() {
  return create<{
    data: { [key: string]: T | null };
    fetchData: (key: string, url: string) => Promise<void>;
  }>((set, get) => ({
    data: {},
    fetchData: async (key, url) => {
      try {
        set((state) => ({ ...state }));

        const response = await fetch(`${API_URL}${url}`);
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();

        set((state) => ({ ...state, data: { ...state.data, [key]: data } }));
      } catch (error) {
        set((state) => ({ ...state }));
      }
    },
  }));
}

// const useDataStore = create<DataStore>((set, get) => ({
//   data: {},
//   isLoading: {},
//   error: {},
//   fetchData: async (key, url) => {
//     try {
//       set((state) => ({
//         ...state,
//         isLoading: { ...state.isLoading, [key]: true },
//         error: { ...state.error, [key]: null },
//       }));

//       const response = await fetch(`${API_URL}${url}`);
//       if (!response.ok) {
//         throw new Error("Network response was not ok");
//       }

//       const data = await response.json();

//       set((state) => ({
//         ...state,
//         data: { ...state.data, [key]: data },
//         isLoading: { ...state.isLoading, [key]: false },
//       }));
//     } catch (error) {
//       set((state) => ({
//         ...state,
//         error: {
//           ...state.error,
//           [key]: (error as Error).message ?? "An error occurred",
//         },
//         isLoading: { ...state.isLoading, [key]: false },
//       }));
//     }
//   },
// }));

export const useDataStore = makeStore<DistrictInfoMap>();
export const useDistrictIndexStore = makeStore<DistrictIndexData>();

const API_URL =
  process.env.REACT_APP_PROD === "yes"
    ? "https://api.district.party/"
    : "http://localhost:5000/";
