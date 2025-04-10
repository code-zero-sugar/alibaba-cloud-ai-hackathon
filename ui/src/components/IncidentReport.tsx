// IncidentReport.jsx
import React from "react";
import { Box, Typography } from "@mui/material";
import PropTypes from "prop-types";
import { IncidentReport as IncidentReportType } from "./models"; // Adjust the import path as necessary

const IncidentReport: React.FC<{ report: IncidentReportType }> = ({ report }) => {
    return (
        <Box
            mt={2}
            sx={{
                border: "1px solid #ccc",
                borderRadius: 1,
                padding: 1,
                backgroundColor: "white",
            }}
        >
            <Typography variant="subtitle1" fontWeight="bold">
                Incident Report
            </Typography>
            <Typography variant="body2">
                <strong>Description:</strong> {report.desc}
            </Typography>
            <Typography variant="body2">
                <strong>Explanation:</strong> {report.explanation}
            </Typography>
            <Typography variant="body2">
                <strong>Action:</strong> {report.action}
            </Typography>
            {report.reported_by && (
                <Typography variant="body2">
                    <strong>Reported By:</strong> {report.reported_by}
                </Typography>
            )}
        </Box>
    );
};

IncidentReport.propTypes = {
    report: PropTypes.shape({
        desc: PropTypes.string.isRequired,
        explanation: PropTypes.string.isRequired,
        action: PropTypes.string.isRequired,
        reported_by: PropTypes.string,
    }).isRequired,
};

export default IncidentReport;
