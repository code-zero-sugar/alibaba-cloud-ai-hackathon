import {
  Typography,
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from "@mui/material";
import { IncidentReportDto } from "./ChatMessage";

type ReportDialogProps = {
  open: boolean;
  handleClose: () => void;
  selectedReport: IncidentReportDto | null;
};

const ReportDialog = ({
  open,
  handleClose,
  selectedReport,
}: ReportDialogProps) => {
  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle
        sx={{
          bgcolor: "primary.main",
          color: "white",
          fontWeight: "bold",
          p: 2,
          borderRadius: "4px 4px 0 0",
        }}
      >
        {selectedReport ? `R-${selectedReport.id} ` : ""}Report Details
      </DialogTitle>
      <DialogContent sx={{ p: 3, mt: 2 }}>
        {selectedReport && (
          <Box>
            <Typography variant="h6" gutterBottom sx={{ fontSize: "1.3rem" }}>
              {selectedReport.desc}
            </Typography>
            <Typography variant="body2" sx={{ mt: 2, fontSize: "1.1rem" }}>
              <strong>Explanation:</strong> {selectedReport.explanation}
            </Typography>
            <Typography variant="body2" sx={{ mt: 1, fontSize: "1.1rem" }}>
              <strong>Action Taken:</strong> {selectedReport.action}
            </Typography>
            {selectedReport.reported_by && (
              <Typography variant="body2" sx={{ mt: 1, fontSize: "1.1rem" }}>
                <strong>Reported By:</strong> {selectedReport.reported_by}
              </Typography>
            )}
            <Typography
              variant="caption"
              sx={{
                mt: 3,
                display: "block",
                color: "text.secondary",
                fontSize: "0.95rem",
              }}
            >
              <strong>Created:</strong>{" "}
              {new Date(selectedReport.created_at).toLocaleString()}
            </Typography>
            <Typography
              variant="caption"
              sx={{
                mt: 0.5,
                display: "block",
                color: "text.secondary",
                fontSize: "0.95rem",
              }}
            >
              <strong>Updated:</strong>{" "}
              {new Date(selectedReport.updated_at).toLocaleString()}
            </Typography>
          </Box>
        )}
      </DialogContent>

      <DialogActions sx={{ p: 2 }}>
        <Button onClick={handleClose} variant="outlined" color="primary">
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ReportDialog;
