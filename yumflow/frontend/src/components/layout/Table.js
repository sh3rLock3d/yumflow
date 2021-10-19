import React, { useState } from "react";


function Table({ df }) {
    df = df['data']
    let cart = df.split('\n')
    cart = cart.map(
        u => u.split(' ').filter(x => x != "")
    )

    console.table(cart)
    const header = cart.shift()

    const footer = cart.pop() + cart.pop()

    return (
        <div class="table-responsive text-left" dir="rtl">
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

export default Table