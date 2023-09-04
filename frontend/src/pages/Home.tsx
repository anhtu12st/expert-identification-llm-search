import React, { Fragment, useState } from 'react'
import { Input, List } from 'antd'
import {
  queryPromptTemplate,
  queryHuggingFace,
  getListScientists,
} from '../services/huggingface'

const { Search } = Input

export const Home: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [listScientists, setListScientists] = useState<any>([])

  const onSearch = async (value: string) => {
    setLoading(true)
    let fullTextList = ''
    try {
      const prompt = queryPromptTemplate(value)
      let response = await queryHuggingFace(prompt)
      prompt.inputs += response
      fullTextList += response
      response = await queryHuggingFace(prompt)
      prompt.inputs += response
      fullTextList += response
      response = await queryHuggingFace(prompt)
      fullTextList += response

      const newListScientists = await getListScientists(fullTextList)
      setListScientists(newListScientists)
    } catch (error) {
    } finally {
      setLoading(false)
    }
  }

  return (
    <Fragment>
      <Search
        placeholder="input search text"
        enterButton="Search"
        size="large"
        onSearch={onSearch}
        disabled={loading}
      />

      <List
        itemLayout="horizontal"
        dataSource={listScientists}
        renderItem={(item: any, index) => (
          <List.Item>
            <List.Item.Meta
              title={`${index + 1}. ${item.name}`}
              description={item.description}
            />
          </List.Item>
        )}
        loading={loading}
      />
    </Fragment>
  )
}
