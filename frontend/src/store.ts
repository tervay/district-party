import { create } from "zustand";
import { DistrictInfoMap } from "./types";

interface DataStore {
  data: DistrictInfoMap; // Change 'any' to the type of your JSON data
  isLoading: { [key: string]: boolean };
  error: { [key: string]: string | null | undefined };
  fetchData: (key: string, url: string) => Promise<void>;
}

const useDataStore = create<DataStore>((set, get) => ({
  data: {},
  isLoading: {},
  error: {},
  fetchData: async (key, url) => {
    try {
      set((state) => ({
        ...state,
        isLoading: { ...state.isLoading, [key]: true },
        error: { ...state.error, [key]: null },
      }));

      const response = await fetch(url);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();

      set((state) => ({
        ...state,
        data: { ...state.data, [key]: data },
        isLoading: { ...state.isLoading, [key]: false },
      }));
    } catch (error) {
      set((state) => ({
        ...state,
        error: {
          ...state.error,
          [key]: (error as Error).message ?? "An error occurred",
        },
        isLoading: { ...state.isLoading, [key]: false },
      }));
    }
  },
}));

export default useDataStore;
