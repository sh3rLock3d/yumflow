import React, { useState, useContext } from "react";
import {
  ActionSetData,
  ActionGetGatheringDataInfo,
  ActionAppendData,
} from "../../actions/Action";
import { Context } from "../../../Store";
import { SET_FLOW } from "../../actions/types";
import Table from "../../layout/Table";
import Snackbar from "../../common/MySnackbar";
import { FormGroup, FormControlLabel, Button, Checkbox } from "@mui/material";

function InsertData({ id }) {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [error, setError] = useState("");

  function InsertDataReq() {
    const data = new FormData();
    data.append(
      "trainData",
      document.getElementById("insert-data-file-input").files[0]
    );
    data.append(
      "addTimeCol",
      document.getElementById("formTimeCol_TrainData").checked
    );

    ActionSetData(id, data)
      .then((data) => data.json())
      .then((data) => {
        console.log(data);
        if (data.message) throw new Error(data.message);
        dispatch({ type: SET_FLOW, payload: data });
      })
      .catch((error) => {
        console.error("Error:", error);
        setError(error.message);
      });
  }

  const form = (
    <form>
      <FormGroup style={{ alignItems: "center" }}>
        <input accept=".csv" hidden id="insert-data-file-input" type="file" />
        <label>لطفا فایل داده‌های خود را به صورت csv آپلود کنید</label>
        <label htmlFor="insert-data-file-input">
          <Button variant="contained" component="span">
            آپلود
          </Button>
        </label>

        <FormControlLabel
          control={<Checkbox color="secondary" id="formTimeCol_TrainData" />}
          label="اضافه کردن ستون زمان به داده‌ها"
        />

        <br />

        <Button
          variant="contained"
          color="success"
          style={{ width: "100%", maxWidth: "300px" }}
          onClick={InsertDataReq}
        >
          ارسال
        </Button>
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
}

function AppendData({ id }) {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [error, setError] = useState("");

  function InsertDataReq() {
    const data = new FormData();
    data.append(
      "trainData",
      document.getElementById("formFile_TrainDataAppend").files[0]
    );
    data.append(
      "addTimeCol",
      document.getElementById("formTimeCol_TrainDataAppend").checked
    );

    ActionAppendData(id, data)
      .then((data) => data.json())
      .then((data) => {
        console.log(data);
        if (data.message) throw new Error(data.message);
        dispatch({ type: SET_FLOW, payload: data });
      })
      .catch((error) => {
        console.error("Error:", error);
        setError(error.message);
      });
  }

  const form = (
    <form>
      <FormGroup style={{ alignItems: "center" }}>
        <input accept=".csv" hidden id="formFile_TrainDataAppend" type="file" />
        <label>
          اضافه کردن داده‌های جدید به داده‌های قبلی (در صورتی که قبلا داده‌ای
          ارسال شده باشد)
        </label>
        <label htmlFor="formFile_TrainDataAppend">
          <Button variant="contained" component="span">
            آپلود
          </Button>
        </label>

        <FormControlLabel
          control={
            <Checkbox color="secondary" id="formTimeCol_TrainDataAppend" />
          }
          label="اضافه کردن ستون زمان به داده‌ها"
        />

        <br />

        <Button
          variant="contained"
          color="success"
          style={{ width: "100%", maxWidth: "300px" }}
          onClick={InsertDataReq}
        >
          ارسال
        </Button>
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
}

function ShowData({ id }) {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [error, setError] = useState("");

  const [chart, setCart] = useState({ state: "hidden", data: null });

  const showData = () => {
    ActionGetGatheringDataInfo(id)
      .then((data) => data.json())
      .then((data) => {
        console.log(data);
        if (data.message) throw new Error(data.message);
        setCart({
          state: "show",
          data: data,
        });
      })
      .catch((error) => {
        console.error("Error:", error);
        setError(error.message);
      });
  };

  const hideData = () => {
    setCart({ state: "hidden", data: null });
  };

  const notShow = (
    <div style={{ display: "flex", justifyContent: "center" }}>
      <Button onClick={showData} variant="contained" style={{ margin: 5 }}>
        مشاهده‌ی جدول
      </Button>
    </div>
  );

  const show = (
    <>
      <div style={{ display: "flex", justifyContent: "center" }}>
        <Button onClick={showData} variant="contained" style={{ margin: 5 }}>
          <i class="bi bi-arrow-repeat"></i>
        </Button>
        <Button onClick={hideData} variant="contained" style={{ margin: 5 }}>
          مخفی کردن جدول
        </Button>
      </div>
      <Table df={chart["data"]} />

      <Snackbar
        open={error}
        onClose={() => setError("")}
        message={error}
        variant="error"
      />
    </>
  );

  return chart["state"] == "hidden" ? notShow : show;
}

function GatheringData() {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  return (
    <div className="container p-2">
      <InsertData id={flow.id} />
      <hr />
      <AppendData id={flow.id} />
      <hr />
      <ShowData id={flow.id} />
    </div>
  );
}

export default GatheringData;
