import express from "express";
import multer from "multer";
import fetch from "node-fetch";
import fs from "fs";
import FormData from "form-data";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();

app.set("view engine", "ejs");
app.use(express.static("public"));

const upload = multer({ dest: "temp_uploads/" });

app.get("/", (req, res) => res.render("index"));

app.post("/upload", upload.single("file"), async (req, res) => {
  try {
    console.log("File received by Node:", req.file?.originalname);

    const formData = new FormData();
    formData.append("file", fs.createReadStream(req.file.path));

    const flaskResponse = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
      headers: formData.getHeaders(),
    });

    const data = await flaskResponse.json();
    res.render("json", { result: data });
  } catch (err) {
    console.error(err);
    res.status(500).send("Error uploading file");
  } finally {
    if (req.file) fs.unlink(req.file.path, () => {});
  }
});

app.listen(3000, () => console.log("Frontend running on http://localhost:3000"));
