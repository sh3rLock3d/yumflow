import React, { useState, useContext } from "react";
import { ActionTestData, ActionGetAllFlowModels } from "../../actions/Action";
import { Context } from "../../../Store";
import Snackbar from "../../common/MySnackbar";

const DataTesting = () => {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [error, setError] = useState("");

  const [flowModels, setFlowModels] = useState(undefined);

  if (!flowModels)
    ActionGetAllFlowModels(flow.id)
      .then((data) => data.json())
      .then((data) => {
        console.log(data);
        setFlowModels(data.models);
      })
      .catch(() => {
        console.log("AAAAAAAA");
      });

  function testDataReq() {
    const data = new FormData();
    data.append(
      "testData",
      document.getElementById("test-flow-models-select").value,
      document.getElementById("formFile_TestData").files[0]
    );

    ActionTestData(flow.id, data)
      .then((data) => data.json())
      .then((data) => {
        console.log(data);
        if (data.message) throw new Error(data.message);
      })
      .catch((error) => {
        console.error("Error:", error);
        setError(error.message);
      });
  }

  const form = (
    <form>
      <select
        className="form-select"
        name="test-flow-models-select"
        id="test-flow-models-select"
      >
        {flowModels &&
          flowModels.map((model) => (
            <option key={model.id} value={model.id}>
              {model.name}
            </option>
          ))}
      </select>
      <div className="form-group text-right">
        <label htmlFor="formFile_TestData">
          داده های خود را به صورت CSV در این جا آپلود کنید
        </label>
        <input
          type="file"
          className="form-control-file"
          id="formFile_TestData"
        />
        <button type="button" className="btn btn-primary" onClick={testDataReq}>
          ارسال
        </button>
      </div>
      <Snackbar
        open={!!error}
        onClose={() => setError("")}
        message={error}
        variant="error"
      />
    </form>
  );

  return form;
};

export default DataTesting;
