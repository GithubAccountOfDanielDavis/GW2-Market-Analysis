import express from 'express'
import { connection } from './entity/utils'
import { getUserById, getUsers, postUserCreation, deleteUser, putUserUpdate } from './controller/user'

// Async to handle initialization
export default (async () => {
  // do not create any routes until TypeORM connection is made
  await connection

  // create and setup express app
  const app = express()
  app.use(express.json())
  app.use(express.urlencoded({ extended: true }))

  app.get('/fetch_new_listings', (req, res) => {
    res.json({ status: 'refreshing' })
  })

  // register routes
  app.get('/api/users', getUsers)
  app.get('/api/users/:id', getUserById)
  app.post('/api/users', postUserCreation)
  app.put('/api/users/:id', putUserUpdate)
  app.delete('/api/users/:id', deleteUser)

  // start express server
  app.listen(3000)
})().catch(e => {
  console.error(e)
})
