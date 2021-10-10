import React, { useState } from "react";
const URL = 'http://127.0.0.1:8000/api/'


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
    const getGatheringDataInfo = `${URL}flows/${project.id}/get_gathering_data_info/`
    React.useEffect(() => {
        fetch(getGatheringDataInfo)
            .then(results => results.json())
            .then(data => {
                setDatas(data);
                console.log(data);
            });
    }, []);


    const listItems = !datas ? <p>loading</p> : dataNames.map((data) =>
        <div className="text-left" dir="ltr" key={data}>
            <p>{data}</p>
            {!datas[data] ? <p>no data set</p>:<ShowData df={datas[data]} />}
            <br />
        </div>
    )

    return <div>
        {listItems}
    </div>

}


function GatheringData({ project }) {
    const setTestAndTrainDataURL = `${URL}flows/${project.id}/set_train_test_data/`
    function setTestAndTrainData() {
        const data = new FormData();
        data.append("train_data", document.getElementById("formFile_TrainData").files[0],)
        data.append("test_data", document.getElementById("formFile_TestData").files[0])
        data.append("label_name", document.getElementById("formFile_labelName").value)


        fetch(setTestAndTrainDataURL, {
            method: 'POST',
            body: data,
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                gatheringDataResult = <GatheringDataResult project={data} />
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }


    const gatheringDataResult = <GatheringDataResult project={project} />

    return (
        <div className="row text-right" id='GatheringDataSection'>
            <div className="container">
                <h1>۱.جمع آوری داده ها</h1>
                <p>برای بارگذاری داده ها چندین روش وجود دارد. یکی از آن ها را انتخاب کنید</p>

                <h3>۱.۱ بارگذاری تمام داده ها</h3>

                <h3>۱.۲ جمع آوری داده های یک وبسایت</h3>

                <h3>۱.۳ بارگذاری داده های تست و ترین به صورت جدا</h3>

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

                {gatheringDataResult}
            </div>
        </div>
    )
}


export default GatheringData