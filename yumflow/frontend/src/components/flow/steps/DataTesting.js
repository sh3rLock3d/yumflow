import React, { useState, useContext } from "react";
import { ActionTestData } from "../../actions/Action";
import { Context } from '../../../Store'

const DataTesting = () => {
    const [state, dispatch] = useContext(Context);
    const flow = state["auth"]["flow"]

    const [error, setError] = useState(false);

    function testDataReq() {
        const data = new FormData();
        data.append("testData", document.getElementById("formFile_TestData").files[0],)

        ActionTestData(flow.id, data)
            .then(data => {
                console.log(data);
            })
            .catch((error) => {
                console.error('Error:', error);
                setError(true);
            });
    }


    const form = <form >
        <div className="form-group text-right">
            <label htmlFor="formFile_TestData">داده های خود را به صورت CSV در این جا آپلود کنید</label>
            <input type="file" className="form-control-file" id="formFile_TestData" />
            <button type="button" className="btn btn-primary" onClick={testDataReq}>ارسال</button>
        </div>
        <Snackbar
          open={error}
          onClose={() => setError(false)}
          message="خطا در ورود!"
          variant="error"
        />
    </form>

    return form
}

export default DataTesting;