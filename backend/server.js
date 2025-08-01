import cors from 'cors'
import mongoose from 'mongoose'
import authRoutes from './routes/auth.js'
import express from 'express'
import dotenv from 'dotenv'
dotenv.config();


const app = express();
app.use(cors());
app.use(express.json());

app.use('/api', authRoutes);

mongoose.connect(process.env.MONGO_URI)
  .then(() => {
    app.listen(process.env.PORT, () => {
      console.log(`Server running on port ${process.env.PORT}`);
    });
  })
  .catch(err => console.log(err));


 