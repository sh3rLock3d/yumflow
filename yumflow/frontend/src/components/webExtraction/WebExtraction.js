import React, { useEffect, useContext } from 'react';
import { Link, Redirect } from 'react-router-dom';
import { Context } from '../../Store'


function WebExtraction() {
    const [state, dispatch] = useContext(Context);

    const onSubmit = (e) => {
        console.log('here')

    };


    return (
        <div className="col-md-6 m-auto">
            <div className="card card-body mt-5">
                <h2 className="text-center">دریافت اطلاعات وب</h2>
                <form onSubmit={onSubmit}>
                    <div className="form-group">
                        <label>آدرس وب</label>
                        <input
                            type="text"
                            
                            className="form-control"
                            name="username"
                        />
                    </div>

                    <div className="form-group">
                        <button type="submit" className="btn btn-primary">
                            دریافت اطلاعات وب
                        </button>
                    </div>

                </form>
            </div>
        </div>
    );
}

export default WebExtraction;
