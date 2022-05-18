import React, { useState, useEffect, useContext } from "react";
import { Context } from "../../../Store";
import { ActionPrepareData, ActionGetAllModels, ActionCreateNewModel } from "../../actions/Action";
import Snackbar from "../../common/MySnackbar";
import {
  FormGroup,
  FormControlLabel,
  Button,
  Radio,
  RadioGroup,
  Select,
  MenuItem,
} from "@mui/material";
import TextField from "../../common/MyTextField";

const CreateModel = () => {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [error, setError] = useState("");


  const create_new_model = () => {
    let name = document.getElementById("new_model_name").value;
    let data = { name };
    ActionCreateNewModel(flow.id, data)
      .then((data) => {
        return data.json();
      })
      .then((data) => {
        if (data.message) throw new Error(data.message);
        console.log(data)
      })
      .catch((error) => {
        setError(error.message);
      });
  }

  const getAllModels = () => {
    ActionGetAllModels(flow.id)
      .then((data) => {
        return data.json();
      })
      .then((data) => {
        if (data.message) throw new Error(data.message);
        console.log(data)
        const options = data.models.map((model) => `<option key=${model.id} value=${model.id}>${model.name}</option>`)
        const sell = document.getElementById("modelSelector")

        sell.innerHTML = options.join('')



      })
      .catch((error) => {
        setError(error.message);
      });
  }


  return (
    <>
      <div className="container p-2 text-center">
        <h5>انتخاب مدل</h5>
        <TextField id="new_model_name" label="مدل جدید" />
        <Button style={{ margin: 5 }} variant="contained" color="primary" onClick={create_new_model}>
          ساخت مدل جدید
        </Button>

        <div className="row m-4">
          <select className="form-select" aria-label="Default select example" id="modelSelector">
          </select>
        </div>

        <Button style={{ margin: 5 }} variant="contained" color="primary" onClick={getAllModels}>
          گرفتن مدل ها
        </Button>


      </div>
    </>
  )
}


const ChooseRows = ({ Pconstraints }) => {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [constraints, setConstraints] = useState({ and: [], or: [] });
  Pconstraints.length = 0;
  Pconstraints.push(...constraints["and"]);
  const addConditionAnd = () => {
    let cname = document.getElementById("chooseRowCol").value;
    if (!cname) return;
    let b =
      "1" == document.getElementById("chooseRowColFormCustomSelect").value;
    let c = constraints["or"];
    document.getElementById("ChooseRowsLogicCondition").value = "==";
    document.getElementById("ChooseRowsvalueCondition").value = "";

    setConstraints({
      and: [...constraints["and"], [cname, b, c]],
      or: [],
    });
  };

  const AndConditions = constraints["and"].map((c, i) => (
    <div key={i} className="my-row" style={{ alignItems: "center" }}>
      <div className="m-1">
        <button
          type="button p-5 m-1"
          onClick={(e) => {
            e.preventDefault();
          }}
          className="btn btn-info"
          dir="ltr"
        >
          {c[0]}
        </button>
        {c[1] ? (
          <button
            type="button p-5 m-1"
            onClick={(e) => {
              e.preventDefault();
            }}
            className="btn btn-info"
            dir="ltr"
          >
            ~
          </button>
        ) : (
          <></>
        )}
      </div>
      <i className="bi bi-arrow-left-short"></i>
      {c[2].map((c, i) => (
        <div key={i}>
          <button
            type="button p-5 m-1"
            onClick={(e) => {
              e.preventDefault();
            }}
            className="btn btn-success"
            dir="ltr"
          >
            {c[0]} {c[1]}
          </button>
          <button
            type="button p-5 m-1"
            onClick={(e) => {
              e.preventDefault();
            }}
            className="btn btn-warning"
            dir="ltr"
          >
            |
          </button>
        </div>
      ))}
    </div>
  ));

  const addConditionOr = () => {
    let logicCondition = document.getElementById(
      "ChooseRowsLogicCondition"
    ).value;
    let valueCondition = document.getElementById(
      "ChooseRowsvalueCondition"
    ).value;
    if (!valueCondition) return;
    document.getElementById("ChooseRowsLogicCondition").value = "==";
    document.getElementById("ChooseRowsvalueCondition").value = "";
    setConstraints({
      and: constraints["and"],
      or: [...constraints["or"], [logicCondition, valueCondition]],
    });
  };
  const notSavedOrs = constraints["or"].map((c, i) => (
    <div key={i}>
      <button
        type="button p-5 m-1"
        onClick={(e) => {
          e.preventDefault();
        }}
        className="btn btn-success"
        dir="ltr"
      >
        {c[0]} {c[1]}
      </button>
      <button
        type="button p-5 m-1"
        onClick={(e) => {
          e.preventDefault();
        }}
        className="btn btn-warning"
        dir="ltr"
      >
        |
      </button>
    </div>
  ));

  return (
    <div className="container p-2 text-center">
      <h5>آماده‌سازی سطرها</h5>
      <p>در این قسمت شرط‌هایی که برای انتخاب یک سطر لازم است را وارد کنید</p>

      <div className="my-row">
        <TextField id="chooseRowCol" label="نام ستون" />

        <Select
          style={{ width: 100 }}
          variant="standard"
          id="chooseRowColFormCustomSelect"
          defaultValue={0}
        >
          <MenuItem value={0}>شرط</MenuItem>
          <MenuItem value={1}>نقیض شرط</MenuItem>
        </Select>
        <i className="bi bi-arrow-left-short"></i>
        <Select
          style={{ width: 100 }}
          variant="standard"
          id="ChooseRowsLogicCondition"
          defaultValue={"=="}
        >
          <MenuItem value={"=="}>==</MenuItem>
          <MenuItem value={"<"}> != </MenuItem>
          <MenuItem value={"!="}> &gt; </MenuItem>
          <MenuItem value={">"}> &lt; </MenuItem>
          <MenuItem value={"isin"}> is in </MenuItem>
          <MenuItem value={"~isin"}> is not in </MenuItem>
        </Select>

        <TextField
          id="ChooseRowsvalueCondition"
          label="مقدار"
          placeholder="'ali', 'hassan', 12.5"
        />
      </div>
      {notSavedOrs}
      <div className="my-row justify-content-center">
        <Button
          style={{ margin: 5 }}
          variant="contained"
          color="primary"
          onClick={addConditionAnd}
        >
          <i className="bi bi-plus-square"></i>
        </Button>
        <Button
          style={{ margin: 5 }}
          variant="contained"
          color="primary"
          onClick={addConditionOr}
        >
          or
        </Button>
      </div>

      <div className="row align-items-center">
        <div className="container">{AndConditions}</div>
      </div>
    </div>
  );
};

const ChooseCols = ({ Pcols }) => {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];
  // cols
  const [inputCols, setInputCols] = useState({});

  Pcols.length = 0;
  Pcols.push(inputCols);

  const inputColDiv = Object.keys(inputCols).map((name) => (
    <div className="row justify-center" key={name}>
      <div className="col-3" id="column_inputs">
        <input
          className="form-control"
          id={name}
          name={name}
          type="text"
          placeholder="نام ستون"
        />
      </div>
    </div>
  ));

  const onkeyupCol = (e) => {
    if (e.keyCode === 13) {
      let k = `columninput${Object.keys(inputCols).length + 1}`;
      let v = e.target.value;
      setInputCols({
        ...inputCols,
        [k]: v,
      });
      return false;
    }
  };

  useEffect(() => {
    for (const item in inputCols) {
      document.getElementById(item).value = inputCols[item];
    }
    document.getElementById("columninput0").value = "";
  }, [inputCols]);

  const [statCols, setStatCols] = useState(1);

  const oncheckColChanged = (e) => {
    let a = e.target.id;
    a = a.charAt(a.length - 1);
    a = parseInt(a);
    setStatCols(a);
  };

  return (
    <div className="container p-2 text-center">
      <h5>آماده‌سازی ستون‌ها</h5>

      <RadioGroup>
        <FormControlLabel
          value="option1"
          control={
            <Radio
              name="radioChooseCol"
              id="radioChooseCol1"
              onChange={oncheckColChanged}
              checked={statCols === 1}
            />
          }
          label="انتخاب تمام ستون‌ها"
        />

        <FormControlLabel
          value="option2"
          control={
            <Radio
              name="radioChooseCol"
              id="radioChooseCol2"
              onChange={oncheckColChanged}
            />
          }
          label="حذف ستون‌های انتخابی"
        />

        <FormControlLabel
          value="option3"
          control={
            <Radio
              name="radioChooseCol"
              id="radioChooseCol3"
              onChange={oncheckColChanged}
            />
          }
          label="انتخاب ستون‌ها"
        />
      </RadioGroup>
      <div style={{ display: statCols === 1 ? "none" : "block" }}>
        {inputColDiv}
        <div className="row justify-center">
          <div className="col-3" id="column_inputs">
            <input
              className="form-control"
              id="columninput0"
              name="columninput0"
              type="text"
              placeholder="نام ستون"
              onKeyUp={onkeyupCol}
            />
          </div>
        </div>
      </div>
    </div>
  );
};


const FillNan = ({PNan}) => {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [inputCols, setInputCols] = useState({});

  PNan.length = 0;
  PNan.push(inputCols);

  const inputColDiv = Object.keys(inputCols).map((name) =>
    <input
      className="form-control"
      id={name}
      name={name}
      type="text"
      defaultValue={inputCols[name]}
      placeholder="نام ستون"
    />
  );


  const addCol = () => {
    let v = document.getElementById("fillNan0").value
    let k = `fillNan${Object.keys(inputCols).length + 1}`;
    document.getElementById("fillNan0").value = ""
    setInputCols({
      ...inputCols,
      [k]: v,
    });
  };

  return (
    <div className="container p-2 text-center">
      <h5>پر کردن سطر های خالی زیر با میانگین</h5>
      <div className="row justify-center">
        <div className="col-3" id="fillNan_inputs">
          {inputColDiv}

          <input
            className="form-control"
            id="fillNan0"
            name="fillNan0"
            type="text"
            placeholder="نام ستون"
          />
        </div>
      </div>

      <Button variant="contained" className="btn btn-info" onClick={addCol}> اضافه کردن ستون </Button>
    </div>
  );

}


const SetCategory = ({Pcategries}) => {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [inputCols, setInputCols] = useState({});
  
  Pcategries.length = 0;
  Pcategries.push(inputCols);
  
  const inputColDiv = Object.keys(inputCols).map((name) =>
    <input
      className="form-control"
      id={name}
      name={name}
      type="text"
      value={inputCols[name]}
      placeholder="نام ستون"
    />
  );


  const addCol = () => {
    let v = document.getElementById("CategoryCol0").value
    let k = `CategoryCol${Object.keys(inputCols).length + 1}`;
    document.getElementById("CategoryCol0").value = ""
    setInputCols({
      ...inputCols,
      [k]: v,
    });
  };

  return (
    <div className="container p-2 text-center">
      <h5>سطر های کتگوری</h5>
      <div className="row justify-center">
        <div className="col-3" id="CategoryCol_inputs">
          {inputColDiv}

          <input
            className="form-control"
            id="CategoryCol0"
            name="CategoryCol0"
            type="text"
            placeholder="نام ستون"
          />
        </div>
      </div>

      <Button variant="contained" className="btn btn-info" onClick={addCol}> اضافه کردن ستون </Button>
    </div>
  )
}


const Normalize = ({Pnormalized}) => {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [inputCols, setInputCols] = useState({});
  
  Pnormalized.length = 0;
  Pnormalized.push(inputCols);
  
  const inputColDiv = Object.keys(inputCols).map((name) =>
    <input
      className="form-control"
      id={name}
      name={name}
      type="text"
      value={inputCols[name]}
      placeholder="نام ستون"
    />
  );


  const addCol = () => {
    let v = document.getElementById("NormalizeCols0").value
    let k = `NormalizeCols${Object.keys(inputCols).length + 1}`;
    document.getElementById("NormalizeCols0").value = ""
    setInputCols({
      ...inputCols,
      [k]: v,
    });
  };

  return (
    <div className="container p-2 text-center">
      <h5>سطر های نرمالایز</h5>
      <div className="row justify-center">
        <div className="col-3" id="CategoryCol_inputs">
          {inputColDiv}

          <input
            className="form-control"
            id="NormalizeCols0"
            name="NormalizeCols0"
            type="text"
            placeholder="نام ستون"
          />
        </div>
      </div>

      <Button variant="contained" className="btn btn-info" onClick={addCol}> اضافه کردن ستون </Button>
    </div>
  )
}


const SliceStr = ({PSliceStr}) => {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [inputCols, setInputCols] = useState({});
  
  PSliceStr.length = 0;
  PSliceStr.push(inputCols);
  
  const inputColDiv = Object.keys(inputCols).map((name) =>
    <input
      className="form-control"
      id={name}
      name={name}
      type="text"
      value={inputCols[name]}
      placeholder="نام ستون"
    />
  );


  const addCol = () => {
    let v = document.getElementById("SliceStrCols0").value
    let k = `SliceStrCols${Object.keys(inputCols).length + 1}`;
    document.getElementById("SliceStrCols0").value = ""
    setInputCols({
      ...inputCols,
      [k]: v,
    });
  };

  return (
    <div className="container p-2 text-center">
      <h5>گرفتن حرف اول سطر ستون ها</h5>
      <div className="row justify-center">
        <div className="col-3" id="CategoryCol_inputs">
          {inputColDiv}

          <input
            className="form-control"
            id="SliceStrCols0"
            name="SliceStrCols0"
            type="text"
            placeholder="نام ستون"
          />
        </div>
      </div>

      <Button variant="contained" className="btn btn-info" onClick={addCol}> اضافه کردن ستون </Button>
    </div>
  )
}


function DataPreparation() {
  const [state, dispatch] = useContext(Context);
  const flow = state["auth"]["flow"];

  const [error, setError] = useState("");

  // rows

  const Pconstraints = [];
  const Pcols = [];
  const Pcategries = [];
  const Pnormalized = [];
  const PNan = [];
  const PSliceStr = [];
  const sendInfo = () => {
    let constraints = Pconstraints;
    let cols = Object.values(Pcols[0]);
    let colFilter = 0;
    if (document.getElementById("radioChooseCol2").checked) {
      colFilter = 1;
    } else if (document.getElementById("radioChooseCol3").checked) {
      colFilter = 2;
    }
    let normalize = Object.values(Pnormalized[0]);
    let nan = Object.values(PNan[0]);
    let category = Object.values(Pcategries[0]);
    let sliceStr = Object.values(PSliceStr[0]);
    var select = document.getElementById("modelSelector")
    let name = Number(select.options[select.selectedIndex].value)
    
    let data = { constraints, cols, colFilter, name, normalize, nan, category, sliceStr};
    console.log(data);
    ActionPrepareData(flow.id, data)
      .then((data) => {
        console.log(data);
        return data.json();
      })
      .then((data) => {
        if (data.message) throw new Error(data.message);
      })
      .catch((error) => {
        setError(error.message);
      });
  };

  return (
    <>
      <CreateModel />
      <hr />

      <form className="container p-2">

        <FormGroup style={{ alignItems: "center" }}>
          <ChooseCols Pcols={Pcols} />
        </FormGroup>
        <hr />
        <FormGroup style={{ alignItems: "center" }}>
          <ChooseRows Pconstraints={Pconstraints} />
        </FormGroup>

        <FormGroup style={{ alignItems: "center" }}>
          <FillNan PNan={PNan}/>
        </FormGroup>

        <FormGroup style={{ alignItems: "center" }}>
          <SliceStr PSliceStr={PSliceStr}/>
        </FormGroup>

        <FormGroup style={{ alignItems: "center" }}>
          <SetCategory Pcategries={Pcategries} />
        </FormGroup>

        <FormGroup style={{ alignItems: "center" }}>
          <Normalize Pnormalized={Pnormalized} />
        </FormGroup>



        <FormGroup style={{ alignItems: "center" }}>
          <Button
            variant="contained"
            color="success"
            style={{ width: "100%", maxWidth: "300px" }}
            onClick={sendInfo}
          >
            ارسال اطلاعات
          </Button>
        </FormGroup>

        <Snackbar
          open={!!error}
          onClose={() => setError("")}
          message={error}
          variant="error"
        />
      </form>
    </>

  );
}

export default DataPreparation;
