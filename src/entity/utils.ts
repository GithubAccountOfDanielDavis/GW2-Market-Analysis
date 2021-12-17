import { validate as performValidation, ValidationError } from 'class-validator'
import { createConnection, DeepPartial, DeleteResult, EntityTarget, InsertResult, Repository } from 'typeorm'
import { QueryDeepPartialEntity } from 'typeorm/query-builder/QueryPartialEntity'
import { Maybe, ok, Result } from '../typescript-monads/'

export const connection = createConnection()

export const useRepository = async <T>(
  target: EntityTarget<T>
): Promise<Repository<T>> => {
  return (await connection).getRepository(target)
}

export const fetchMany = async <T>(
  entity: EntityTarget<T>
): Promise<T[]> => {
  const repo = await useRepository(entity)
  return await repo.find()
}

export const fetchOne =
  <T>(entity: EntityTarget<T>) =>
    async (id: number): Promise<Maybe<T>> => {
      const repo = await useRepository(entity)
      const oneOrUndefined = await repo.findOne(id)
      return new Maybe(oneOrUndefined)
    }

export const validate = async <T>(
  entity: T
): Promise<Result<T, ValidationError[]>> => {
  const errors = await performValidation(entity as Record<string, unknown>)
  return (errors.length > 0)
    ? fail(errors)
    : ok(entity)
}

export const build =
  <T>(entity: EntityTarget<T>) =>
    async (params: unknown): Promise<T> => {
      const repo = await useRepository(entity)
      return repo.create(params as DeepPartial<T>)
    }

export const deleteOne =
  <T extends Record<string, unknown>>(entity: EntityTarget<T>) =>
    async (id: number): Promise<DeleteResult> => {
      const repo = await useRepository(entity)
      return await repo.delete(id)
    }

export const insertOne =
  <T>(entity: EntityTarget<T>) =>
    async (t: QueryDeepPartialEntity<T>): Promise<InsertResult> => {
      const repo = await useRepository(entity)
      return await repo.insert(t)
    }

export const merge =
  <T>(entity: EntityTarget<T>, updates: unknown) =>
    async (original: T): Promise<T> => {
      const repo = await useRepository(entity)
      return repo.merge(original, updates as DeepPartial<T>)
    }

export const updateOne =
  <T>(entity: EntityTarget<T>) =>
    async (t: T): Promise<T> => {
      const repo = await useRepository(entity)
      return await repo.save(t)
    }
