# Create your views here.


class OwnedModelViewMixin(object):
    """Mixing for owned models"""
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return super(OwnedModelViewMixin, self).\
            form_valid(form)