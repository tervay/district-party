import { Route, Switch } from "wouter";
import Landing from "./Landing";
import District from "./district";

export default function Routing(): JSX.Element {
  // const { data, isLoading } = useDataStore();
  // if (isLoading) {
  //   return (
  //     <Route path="/">
  //       <Landing />
  //     </Route>
  //   );
  // }

  return (
    <Switch>
      <Route path="/">
        <Landing />
      </Route>

      <Route path="/d/:districtKey">
        {(params) => <District districtKey={params.districtKey} />}
      </Route>
    </Switch>
  );
}
