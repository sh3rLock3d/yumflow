import React, { useState } from "react";
import { ActionSetSepetatedTestTrainData, ActionGetGatheringDataInfo } from "../../actions/Action";


const AllData = "تمامی داده ها"
const SepetatedTestTrainData = "داده های آمورش و تست به صورت جداگانه"
const InstaData = "وارد کردن داده های صفحه ی اینستاگرام"
const CrawlWeb = "استخراج داده های وب"


function AllDataDiv({ selectedFlow, setSelectedFlow }) {
    return (
        <p>
            im new {AllData}
        </p>
    )
}


function SepetatedTestTrainDataDiv({ selectedFlow, setSelectedFlow }) {

    function setTestAndTrainData() {
        const data = new FormData();
        data.append("train_data", document.getElementById("formFile_TrainData").files[0],)
        data.append("test_data", document.getElementById("formFile_TestData").files[0])
        data.append("label_name", document.getElementById("formFile_labelName").value)

        ActionSetSepetatedTestTrainData(selectedFlow.id, data)
            .then(data => {
                console.log('Success:', data);
                gatheringDataResult = <GatheringDataResult project={data} />
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    return (
        <div className="container">
            <div className="row">
                <div className="col-sm">
                    <div className="mb-3" dir="ltr">
                        <label htmlFor="formFile_TrainData" className="form-label">
                            داده های آموزش
                        </label>
                        <input className="form-control" type="file" id="formFile_TrainData" />
                    </div>
                </div>
                <div className="col-sm">
                    <div className="mb-3" dir="ltr">
                        <label htmlFor="formFile_TestData" className="form-label">
                            داده های تست
                        </label>
                        <input className="form-control" type="file" id="formFile_TestData" />
                    </div>
                </div>
            </div>

            <div className="row">
                <div className="col-sm">
                    <label htmlFor="formFile_labelName">نام برچسب</label>
                    <input type="text" className="form-control" dir="ltr" id="formFile_labelName" placeholder="lable1, lable2, ..." />
                </div>
                <div className="col-sm ">
                    <button type="button" className="btn btn-primary float-left" onClick={setTestAndTrainData}>ارسال</button>
                </div>
            </div>
        </div>

    )
}


function InstaDataDiv({ selectedFlow, setSelectedFlow }) {
    return (
        <p>
            im new {InstaData}
        </p>
    )
}


function CrawlWebDiv({ selectedFlow, setSelectedFlow }) {
    return (
        <p>
            im new {CrawlWeb}
        </p>
    )
}


function ShowData({ df }) {

    let cart = df.split('\n')
    cart = cart.map(
        u => u.split(' ').filter(x => x != "")
    )

    console.table(cart)
    const header = cart.shift()

    const footer = cart.pop() + cart.pop()

    return (
        <div class="table-responsive">
            <table class="table">
                <thead class="thead-dark">
                    <tr>
                        <th scope="col">-</th>
                        {
                            header.map((row) => <th scope="col">{row}</th>)
                        }
                    </tr>
                </thead>
                <tbody>
                    {
                        cart.map((row) =>
                            <tr>
                                {<th scope="row">{row.shift()}</th>}
                                {row.map(element => <td>{element}</td>)}
                            </tr>
                        )
                    }
                </tbody>
            </table>

        </div>
    )

}

function GatheringDataResult({ project }) {
    const dataNames = [
        'x_train',
        'y_train',
        'x_test',
        'y_test',
    ]
    const [datas, setDatas] = React.useState(null);

    const showData = () => {
        ActionGetGatheringDataInfo(project.id)
            .then(data => {
                setDatas(data);
                console.log(data);
            });
    }


    const listItems = !datas ? <p>loading</p> : dataNames.map((data) =>
        <div className="text-left" dir="ltr" key={data}>
            <p>{data}</p>
            {!datas[data] ? <p>no data set</p> : <ShowData df={datas[data]} />}
            <br />
        </div>
    )

    return <div class="accordion" id="accordionPanelsStayOpenExample">
        <div class="accordion-item">
            <h2 class="accordion-header" id="panelsStayOpen-headingOne">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapseOne" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
                    Accordion Item #1
                </button>
            </h2>
            <div id="panelsStayOpen-collapseOne" class="accordion-collapse collapse show" aria-labelledby="panelsStayOpen-headingOne">
                <div class="accordion-body">
                    {listItems}
                </div>
            </div>
        </div>
    </div>
}

function GatheringData({ selectedFlow, setSelectedFlow }) {


    const [insertData, setInsertData] = useState(null)

    const makeInsertDataDiv = (item) => {
        switch (item) {
            case AllData:
                setInsertData(<AllDataDiv selectedFlow={selectedFlow} setSelectedFlow={setSelectedFlow} />)
                break;
            case SepetatedTestTrainData:
                setInsertData(<SepetatedTestTrainDataDiv selectedFlow={selectedFlow} setSelectedFlow={setSelectedFlow} />)
                break;
            case InstaData:
                setInsertData(<InstaDataDiv selectedFlow={selectedFlow} setSelectedFlow={setSelectedFlow} />)
                break;
            case CrawlWeb:
                setInsertData(<CrawlWebDiv selectedFlow={selectedFlow} setSelectedFlow={setSelectedFlow} />)
                break;
            default:

        }
    }

    return (
        <div className="container p-2">
            <div className="dropdown float-right" >
                <button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    نوع ایجاد داده را انتخاب کنید
                </button>
                <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                    <a className="dropdown-item text-right" onClick={() => { makeInsertDataDiv(AllData) }} >{AllData}</a>
                    <a className="dropdown-item text-right" onClick={() => { makeInsertDataDiv(SepetatedTestTrainData) }}>{SepetatedTestTrainData}</a>
                    <a className="dropdown-item text-right" onClick={() => { makeInsertDataDiv(InstaData) }}>{InstaData}</a>
                    <a className="dropdown-item text-right" onClick={() => { makeInsertDataDiv(CrawlWeb) }}>{CrawlWeb}</a>
                </div>
            </div>

            <br />
            <br />

            {insertData}

            {
                /*
                <GatheringDataResult project={selectedFlow} />
                */
            }
            


        </div>

    )
}


export default GatheringData