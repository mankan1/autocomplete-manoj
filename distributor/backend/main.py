import falcon
import json
import logging
from backend import Backend, NodeInactiveError


class MainResourceCount(object):
	def __init__(self):
		self._logger = logging.getLogger('gunicorn.error')
		self._backend = Backend()
		self._backend.start()

	def on_get(self, req, resp):
		self._logger.debug(f'Handling {req.method} request {req.url} with params {req.params}')
		try:
			count_top_phrases = self._backend.count_top_phrases_for_prefix(req.params['prefix'])
			response_body = json.dumps(
				{
					"status": "success",
					"data": {
						"count-top-phrases": count_top_phrases 
					}
				 })
			resp.status = falcon.HTTP_200
			resp.body = response_body

		except NodeInactiveError as err:
			response_body = json.dumps(
				{
					"status": "error",
					"message": "This backend node is not active. Consult zookeeper for the most recent active nodes"
				 })
			resp.status = falcon.HTTP_500
			resp.body = response_body

		except Exception as e:
			self._logger.error('An error occurred when processing the request', exc_info=e)
			response_body = json.dumps(
				{
					"status": "error",
					"message": "An error occurred when processing the request"
				 })
			resp.status = falcon.HTTP_500
			resp.body = response_body

		
class MainResource(object):
	def __init__(self):
		self._logger = logging.getLogger('gunicorn.error')
		self._backend = Backend()
		self._backend.start()

	def on_get(self, req, resp):
		self._logger.debug(f'Handling {req.method} request {req.url} with params {req.params}')
		try:
			top_phrases = self._backend.top_phrases_for_prefix(req.params['prefix'])
			response_body = json.dumps(
				{
					"status": "success",
					"data": {
						"top_phrases": top_phrases 
					}
				 })
			resp.status = falcon.HTTP_200
			resp.body = response_body

		except NodeInactiveError as err:
			response_body = json.dumps(
				{
					"status": "error",
					"message": "This backend node is not active. Consult zookeeper for the most recent active nodes"
				 })
			resp.status = falcon.HTTP_500
			resp.body = response_body

		except Exception as e:
			self._logger.error('An error occurred when processing the request', exc_info=e)
			response_body = json.dumps(
				{
					"status": "error",
					"message": "An error occurred when processing the request"
				 })
			resp.status = falcon.HTTP_500
			resp.body = response_body

		


app = falcon.API()
main_resource = MainResource()
main_resource_count = MainResourceCount()

app.add_route('/top-phrases', main_resource)

app.add_route('/count-top-phrases', main_resource_count)
