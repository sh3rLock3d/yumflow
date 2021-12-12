import React, { useEffect, useContext } from "react";
import { Context } from "../../Store";

function Homepage() {
  const [state, dispatch] = useContext(Context);
  console.log(state);

  return (
    <div className="container-fluid welcome-message">
      <h2 style={{ width: "fit-content" }}>
        Welcome{state.auth.isAuthenticated && ` ${state.auth.user.username}`}!
      </h2>
    </div>
  );
}

export default Homepage;
