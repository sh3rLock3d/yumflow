import React, { Component, useState, useContext } from "react";
import { ActionGetAllModels, ActionGetTrainAndTestInfo } from "../../actions/Action";
import { Context } from "../../../Store";
import Snackbar from "../../common/MySnackbar";
import { Button } from "@mui/material";
import BuildNetwork from "./network/BuildNetwork";

class Table extends Component {
    render() {
        var heading = this.props.heading;
        var body = this.props.body;
        return (
            <table  style={{ width: 500 }}>
                <thead>
                    <tr>
                        {heading.map(head => <th>{head}</th>)}
                    </tr>
                </thead>
                <tbody>
                    {body.map(row => <TableRow row={row} />)}
                </tbody>
            </table>
        );
    }
}

class TableRow extends Component {
    render() {
        var row = this.props.row;
        return (
            <tr>
                {row.map(val => <td>{val}</td>)}
            </tr>
        )
    }
}
const DataTable = ({ data }) => {
    console.log(data)
    const body = []

    for (let i = 0; i < data['colType'].length; i++) {
        body.push([data['colType'][i], data['columnsName'][i]])
    }
    return (<>
        <p>سایز داده {data.shape[0]} در {data.shape[1]}</p>
        <Table heading={['colType', 'columnsName']} body={body} />,
    </>)
}








const CreateModel = () => {
    const [state, dispatch] = useContext(Context);
    const flow = state["auth"]["flow"];


    const [datainfo, setdatainfo] = useState({ 'test': null, 'train': null });

    const getAllModels = () => {
        ActionGetAllModels(flow.id)
            .then((data) => {
                return data.json();
            })
            .then((data) => {
                if (data.message) throw new Error(data.message);
                console.log(data)
                const options = data.models.map((model) => `<option key=${model.id} value=${model.id}>${model.name}</option>`)
                const sell = document.getElementById("modelSelectormodel")
                sell.innerHTML = options.join('')
            })
            .catch((error) => {
                setError(error.message);
            });
    }

    const getInfoOfTrainAndTest = () => {
        var select = document.getElementById("modelSelectormodel")
        let modelId = Number(select.options[select.selectedIndex].value)
        const data = { modelId }
        console.log(data)
        ActionGetTrainAndTestInfo(flow.id, data)
            .then((data) => {
                return data.json();
            })
            .then((data) => {
                if (data.message) throw new Error(data.message);
                setdatainfo(data)

            })
            .catch((error) => {
                setError(error.message);
            });
    }

    const dataTables = datainfo.test == null ? <></> : <div class="container">
        <div className="row">
            <div className="col-6">
                <h5>داده تست</h5>
                <DataTable data={datainfo.test} />
            </div>
            <div className="col-6">
                <h5>داده آموزش</h5>
                <DataTable data={datainfo.train} />
            </div>
        </div>
    </div>


    const [error, setError] = useState("");
    return (
        <div className="container p-2 text-center">
            <h5>انتخاب مدل</h5>
            <div className="row m-4">
                <select className="form-select" aria-label="Default select example" id="modelSelectormodel">
                </select>
            </div>
            <Button style={{ margin: 5 }} variant="contained" color="primary" onClick={getAllModels}>
                گرفتن مدل ها
            </Button>
            <hr />
            <h5>اطلاعات داده ی تست و آموزش</h5>
            <Button style={{ margin: 5 }} variant="contained" color="primary" onClick={getInfoOfTrainAndTest}>گرفتن اطلاعات  </Button>
            {
                dataTables
            }
            <hr />
            <BuildNetwork />
        </div>

    )

};

export default CreateModel;
