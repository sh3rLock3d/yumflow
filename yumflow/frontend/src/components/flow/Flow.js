import React, { useState, useContext } from "react";
import { useParams } from "react-router-dom";
import { Context } from "../../Store";
import { ActionGetFlow } from "../actions/Action";
import { SET_FLOW } from "../actions/types";
import Snackbar from "../common/MySnackbar";

import GatheringData from "./steps/GatheringData";
import DataPreparation from "./steps/DataPreparation";
import DataTraining from "./steps/DataTraining";
import DataTesting from "./steps/DataTesting";

const Flow = () => {
  const { id } = useParams();
  const [error, setError] = useState(false);

  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];
  if (!flow || id != flow.id) {
    ActionGetFlow(id)
      .then((data) => data.json())
      .then((data) => {
        if (data.message) throw new Error(data.message);
        dispatch({ type: SET_FLOW, payload: data });
      })
      .catch((error) => {
        setError(error.message);
      });

    return <p>loading...</p>;
  }

  return (
    <div className="row justify-content-center">
      <div
        id="accordion"
        className="col-8 align-self-center accordion"
        style={{ padding: 0 }}
      >
        <div className="accordion-item">
          <h1 className="accordion-header" id="headingOne">
            <button
              className="accordion-button"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#collapseOne"
              aria-expanded="true"
              aria-controls="collapseOne"
            >
              ۱.جمع‌آوری داده‌ها
            </button>
          </h1>

          <div
            id="collapseOne"
            className="accordion-collapse collapse show"
            aria-labelledby="headingOne"
            data-bs-parent="#accordion"
          >
            <GatheringData />
          </div>
        </div>

        <div className="accordion-item">
          <h1 className="accordion-header" id="headingTwo">
            <button
              className="accordion-button collapsed"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#collapseTwo"
              aria-expanded="false"
              aria-controls="collapseTwo"
            >
              ۲.آماده‌سازی داده‌ها
            </button>
          </h1>

          <div
            id="collapseTwo"
            className="accordion-collapse collapse"
            aria-labelledby="headingTwo"
            data-bs-parent="#accordion"
          >
            <DataPreparation />
          </div>
        </div>

        <div className="accordion-item">
          <h1 className="accordion-header" id="headingThree">
            <button
              className="accordion-button collapsed"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#collapseThree"
              aria-expanded="false"
              aria-controls="collapseThree"
            >
              ۳. آموزش داده‌ها
            </button>
          </h1>

          <div
            id="collapseThree"
            className="accordion-collapse collapse"
            aria-labelledby="headingThree"
            data-bs-parent="#accordion"
          >
            <DataTraining />
          </div>
        </div>

        <div className="accordion-item">
          <h1 className="accordion-header" id="headingFour">
            <button
              className="accordion-button collapsed"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#collapseFour"
              aria-expanded="false"
              aria-controls="collapseFour"
            >
              ۴. تست داده‌ها
            </button>
          </h1>

          <div
            id="collapseFour"
            className="accordion-collapse collapse"
            aria-labelledby="headingFour"
            data-bs-parent="#accordion"
          >
            <DataTesting />
          </div>
        </div>
      </div>

      <Snackbar
        open={!!error}
        onClose={() => setError("")}
        message={error}
        variant="error"
      />
    </div>
  );
};

export default Flow;
