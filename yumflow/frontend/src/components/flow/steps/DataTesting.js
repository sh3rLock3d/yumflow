import React, { useState, useContext } from "react";
import { ActionTestData, ActionGetAllFlowModels } from "../../actions/Action";
import { Context } from "../../../Store";
import Snackbar from "../../common/MySnackbar";
import { FormGroup, Button, Select, MenuItem } from "@mui/material";

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
      <FormGroup className="container p-2" style={{ alignItems: "center" }}>
        <div className="my-row">
          <Select
            style={{ width: 100 }}
            variant="standard"
            id="test-flow-models-select"
          >
            {flowModels &&
              flowModels.map((model) => (
                <MenuItem key={model.id} value={model.id}>
                  {model.name}
                </MenuItem>
              ))}
          </Select>
        </div>

        <input accept=".csv" hidden id="formFile_TestData" type="file" />
        <label>لطفا فایل داده‌های خود را به صورت csv آپلود کنید</label>
        <label htmlFor="formFile_TestData">
          <Button variant="contained" component="span">
            آپلود
          </Button>
        </label>

        <br />
        <Button
          variant="contained"
          color="success"
          style={{ width: "100%", maxWidth: "300px" }}
          onClick={testDataReq}
        >
          ارسال
        </Button>
        <br />
      </FormGroup>

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
