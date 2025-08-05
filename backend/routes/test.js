


const router = express.Router();

router.get('/dashboard', authMiddleware, async (req, res) => {
  
  res.json({ message: 'Welcome to your dashboard!' });
});