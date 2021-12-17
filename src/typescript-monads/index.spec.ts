import { maybe, Maybe, ok, fail, Result } from './'

describe('package api', () => {
  it('should export maybe', () => {
    expect(maybe(1)).toBeInstanceOf(Maybe)
  })

  it('should export result', () => {
    expect(ok(1)).toBeInstanceOf(Result)
    expect(fail(1)).toBeInstanceOf(Result)
  })
})
