import { Context } from "../../../Store";
import { ActionCompareAllModels, } from "../../actions/Action";
import React, { Component, useState, useContext } from "react";
import { Button } from "@mui/material";



function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

class Table extends Component {
    render() {
        var heading = this.props.heading;
        var body = this.props.body;
        return (
            <table style={{ width: 500 }}>
                <thead>
                    <tr>
                        {heading.map((head, i) => <th key={i}>{head}</th>)}
                    </tr>
                </thead>
                <tbody>
                    {body.map((row, i) => <TableRow key={i} row={row} />)}
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
                {row.map((val, i) => <td key={i}>{val}</td>)}
            </tr>
        )
    }
}
const DataTable = ({ data }) => {
    const body = []

    for (let i = 0; i < data.length; i++) {
        body.push([data[i]['name'], data[i]['loss_fn'],data[i]['accuracy'], data[i]['avgLoss']])
    }
    return (<>
        <Table heading={['name', 'loss_fn', 'accuracy', 'avgLoss']} body={body} />,
    </>)
}


const CompareModel = () => {
    const [state, dispatch] = useContext(Context);
    const flow = state["auth"]["flow"];
    const [datainfo, setdatainfo] = useState({ 'data': null, });
    const getAllModels = () => {
        ActionCompareAllModels(flow.id)
            .then((data) => {
                return data.json();
            })
            .then((data) => {
                if (data.message) throw new Error(data.message);
                console.log(data)
                setdatainfo({'data':data.models})

            })
            .catch((error) => {

            });
    }
    
    const dataTable = datainfo.data == null ? <></> : <div className="container">
        <div className="row">
            <div className="col">
                <h5>مدل ها</h5>
                <DataTable data={datainfo.data} />
            </div>
        </div>
    </div>


    return (
        <>
            <Button style={{ margin: 5 }} variant="contained" color="primary" onClick={getAllModels}>
                مقایسه مدل ها
            </Button>
            {dataTable}

        </>
    );
};

export default CompareModel;
