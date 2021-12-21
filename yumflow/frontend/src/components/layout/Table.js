import React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";

function MyTable({ tableData }) {
  return (
    <Table sx={{ minWidth: 650 }}>
      <TableHead>
        <TableRow>
          {tableData.header.map((h, index) => (
            <TableCell key={`header-${index}`}>{h}</TableCell>
          ))}
        </TableRow>
      </TableHead>
      <TableBody>
        {tableData.data[0].map((_, index) => (
          <TableRow
            key={`row-${index}`}
            sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
          >
            {tableData.data.map((dataCol, index2) => (
              <TableCell align="right" key={`cell-${index}-${index2}`}>
                {dataCol[index]}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}

export default MyTable;
