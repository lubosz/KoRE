/*
  Copyright © 2012 The KoRE Project

  This file is part of KoRE.

  KoRE is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  KoRE is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with KoRE.  If not, see <http://www.gnu.org/licenses/>.
*/
#include "KoRE/Operations/BindAttribute.h"

kore::BindAttribute::BindAttribute(void) : _meshAttPtr(NULL),
                                               _shaderInput(NULL),
                                               kore::Operation() {
}

kore::BindAttribute::BindAttribute(const kore::MeshAttributeArray& meshAtt,
                                       const kore::ShaderInput& shaderAtt) :
                                      _meshAttPtr(&meshAtt),
                                      _shaderInput(&shaderAtt),
                                      kore::Operation() {
}


kore::BindAttribute::~BindAttribute(void) {
}

void kore::BindAttribute::execute(void) {
  glEnableVertexAttribArray(_shaderInput->location);
  glVertexAttribPointer(_shaderInput->location, _meshAttPtr->numComponents,
      _meshAttPtr->componentType, GL_FALSE, 0, _meshAttPtr->data);
}

void kore::BindAttribute::update(void) {
}

void kore::BindAttribute::reset(void) {
}

void kore::BindAttribute::connect(const kore::MeshAttributeArray& meshAtt,
                                    const kore::ShaderInput& shaderAtt) {
  _meshAttPtr = &meshAtt;
  _shaderInput = &shaderAtt;
}
