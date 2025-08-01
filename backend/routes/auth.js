import { User } from '../models/user.js';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import express from 'express';

const router = express.Router();

router.post('/register', async (req, res) => {
  try {
    const { email, password } = req.body;

    const existing = await User.findOne({ email });
    if (existing) return res.status(400).json({ message: 'User exists' });

    const hashed = await bcrypt.hash(password, 10);
    const newUser = await User.create({ email, password: hashed });

    return res.status(201).json({ message: 'User created', userId: newUser._id });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ message: 'Server error' });
  }
});

router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    const user = await User.findOne({ email });
    if (!user) return res.status(401).json({ message: 'Invalid credentials' });

    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) return res.status(401).json({ message: 'Invalid credentials' });

    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '1h' });

    return res.status(200).json({
      token,
      email: user.email,
      id: user._id
    });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ message: 'Server error' });
  }
});

export default router;
