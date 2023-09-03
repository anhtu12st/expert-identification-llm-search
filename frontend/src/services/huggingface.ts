export interface QueryType {
  inputs: string
  parameters?: any
}

export async function queryHuggingFace(data: QueryType) {
  const response = await fetch(
    'https://clwvsfzz92fhsvxq.us-east-1.aws.endpoints.huggingface.cloud',
    {
      headers: {
        Authorization:
          'Bearer ZHqvvSXlVpPKannRbwlRMehlxcKZtuQdrRGCQYZGnnGHPDVzAHLLwGIeagKxYisKjDUusFkYlTAuYSxVXEHdkocHfYpsetIrMhqSgzxRySPWoKzpXQzMpmEDoLzbJAmN',
        'Content-Type': 'application/json',
      },
      method: 'POST',
      body: JSON.stringify(data),
    }
  )
  const result = await response.json()
  return result[0].generated_text
}

export const queryPromptTemplate = (text: string): QueryType => {
  const prompt = `
Customer have list of technology and the following is an agent that recommends scientists relevant to a customer. The agent is responsible to recommend a list of name only from the top scientist. List names only. DO NOT PUT ANY EXTRA INFORMATION.
Customer: ${text}
Agent:

`
  return {
    inputs: prompt,
    parameters: {
      repetition_penalty: 1.0,
      max_length: 1024,
    },
  }
}

export const queryScientistTemplate = (name: string): QueryType => {
  const prompt = `
Describe scientist ${name} in 50 words only:

`
  return { inputs: prompt }
}

export const getListScientists = async (response: string): Promise<any[]> => {
  const listScientistsName = response
    .split('\n')
    .map((s) => s.trim().split(' ').slice(1).join(' '))
    .filter((s) => !!s)
  const listScientistsPromise = listScientistsName.map(async (name) => {
    const prompt = queryScientistTemplate(name)
    const res = await queryHuggingFace(prompt)
    return { name, description: res }
  })
  const listScientists = await Promise.all(listScientistsPromise)
  return listScientists
}
