const express = require('express');
const router = express.Router();
const {
  getTasks,
  getTask,
  createTask,
  updateTask,
  deleteTask
} = require('../../controllers/taskController');
const { protect } = require('../../middlewares/authMiddleware');
const { validate, taskSchema } = require('../../middlewares/validateMiddleware');

// Route for /api/v1/tasks
router.route('/')
  .get(protect, getTasks)
  .post(protect, validate(taskSchema), createTask);

router.route('/:id')
  .get(protect, getTask)
  .put(protect, validate(taskSchema), updateTask)
  .delete(protect, deleteTask);

module.exports = router;
